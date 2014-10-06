def download_file(url, blocksize=1024):
    with open(filename, 'wb') as handle:
        response = requests.get(url, stream=True)

        if not response.ok:
            return False

        for block in response.iter_content(blocksize):
            if not block:
                break
            handle.write(block)
