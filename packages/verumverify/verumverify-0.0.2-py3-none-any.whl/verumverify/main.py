import click

from . import crypto_svc, retrieval_svc, status_svc, video_svc


@click.command(no_args_is_help=True)
@click.option('--hash_id',
              help='The hash of a recording from Verum.')
@click.option('--url',
              help='A url of a Verum file.')
@click.option('--id',
              help='ID if a recording from Verum.')
@click.option('--videofile',
              help='A raw recording MP4 file.')
@click.option('--zipfile',
              help='local path to a zip file from a Verum recording.')
@click.option('--host', default="https://verumjourno.com",
              help="The verum server. Defaults to https://verumjourno.com")
@click.option('-v', '--verbose', count=True,
              help="More information out")
@click.option('-p', '--preserve', is_flag=True,
              help="Preserve downloaded artifacts")
def main(hash_id, url, id, zipfile, videofile, host, verbose, preserve):
    """Verify the cryptographic authenticity of a Verum recording."""
    if not any((hash_id, url, id, zipfile, videofile)):
        return

    if hash_id:
        status_svc.start(f"\nVerify Authenticity of Hash: {hash_id}\n",
                         nl=True)
        status_svc.start("Locating and retrieving files")
        fetched = retrieval_svc.get_by_hash_id(hash_id, host)
    elif id:
        status_svc.start(f"\nVerify Authenticity of Recording ID: {id}\n",
                         nl=True)
        status_svc.start("Locating and retrieving files")
        fetched = retrieval_svc.get_by_uuid(id, host)
    elif url:
        status_svc.start(f"\nVerify Authenticity of Url: {url}\n",
                         nl=True)
        status_svc.start("Locating and retrieving files")
        fetched = retrieval_svc.get_by_url(url)
    elif videofile:
        status_svc.start(f"\nVerify Authenticity of Video: {videofile}\n",
                         nl=True)
        status_svc.start("Computing Video File Hash")
        status_svc.prog()
        status_svc.success()
        hash_id = video_svc.compute_hash_from_path(videofile)
        status_svc.start(f"Locating and retrieving files for hash: {hash_id}")
        fetched = retrieval_svc.get_by_hash_id(hash_id, host)
    else:
        status_svc.start(f"\nVerify Authenticity of Zip File: {zipfile}\n",
                         nl=True)
        status_svc.start("Locating and retrieving files")
        fetched = retrieval_svc.get_by_zip(zipfile)
    status_svc.prog()
    if not fetched:
        status_svc.fail()
        status_svc.start(f"No Video Matched for Hash: {hash_id}", nl=True)
        return
    status_svc.success()

    status_svc.start("Loading data and signature files")
    file_map = retrieval_svc.gather()
    status_svc.prog()
    status_svc.success()

    status_svc.start("Loading public key files")
    device_key = retrieval_svc.load_key("device.pem")
    verum_key = retrieval_svc.load_key("verum.pem")
    status_svc.prog()
    if device_key and verum_key:
        status_svc.success()
    else:
        status_svc.fail()
        return

    _data = file_map['timestamps']
    tsr = retrieval_svc.load_file(_data['tsr'])
    time_from_tsr = crypto_svc.time_from_tsr(tsr)

    device = retrieval_svc.extract_data(file_map, "device")
    recording = retrieval_svc.extract_data(file_map, "recording")
    variant = device['variant']

    click.secho(f"""
        Video '{recording["name"]}' was recording on
        an {variant.title()} {device[variant]['device'].upper()} on {device[variant]['brand'].title()}
        called {device['name']}
        at around {time_from_tsr}.

        The Hash ID is: {recording['hash_id']}
    """)

    for category, _data in file_map.items():
        c_data = retrieval_svc.extract_data(file_map, category)
        _verify(category, _data, device_key, verum_key, c_data)

    if not preserve:
        retrieval_svc.clear()


def _verify(category, _data, device_key, verum_key, c_data):
    status_svc.start(f"Verifying {category.title()} Authenticity", nl=True)
    if category == "timestamps":
        tsq = retrieval_svc.load_file(_data['tsq'])
        tsr = retrieval_svc.load_file(_data['tsr'])
        time_from_tsr = crypto_svc.time_from_tsr(tsr)
        is_authentic = crypto_svc.verify_ts(tsr, tsq)
        status_svc.start(f"{time_from_tsr}")
        status_svc.prog()
        if is_authentic:
            status_svc.success()
        else:
            status_svc.fail()

    else:
        for uuid, packet in _data.items():
            _cat_name = (category
                         if category in {"recording", "device"} else
                         c_data[uuid]['channel'])

            status_svc.start(f"| {_cat_name} |")

            is_authentic_device = crypto_svc.verified(
                retrieval_svc.load_file(packet['data']),
                retrieval_svc.load_file(packet['device']),
                device_key,
            )
            status_svc.prog(cnt=1)
            is_authentic_verum = crypto_svc.verified(
                retrieval_svc.load_file(packet['data']),
                retrieval_svc.load_file(packet['verum']),
                verum_key,
            )
            status_svc.prog(cnt=1)
            if is_authentic_device and is_authentic_verum:
                status_svc.prog(cnt=1)
                status_svc.success()
            else:
                status_svc.fail()


if __name__ == '__main__':
    main()
