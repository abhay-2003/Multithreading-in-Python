import os
import time
import threading
import urllib.request
from urllib.parse import urlparse


def download_file(url, filename):
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"Downloaded: {filename}")
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False


def download_sequential(urls):
    print("\nStarting sequential download...")
    start = time.time()
    for i, url in enumerate(urls):
        filename = f"seq_file_{i+1}{os.path.splitext(urlparse(url).path)[-1] or '.bin'}"
        download_file(url, filename)
    end = time.time()
    print(f"Sequential download time: {end - start:.2f} seconds")
    return end - start


def download_concurrent(urls):
    print("\nStarting concurrent download using threads...")
    start = time.time()
    threads = []
    for i, url in enumerate(urls):
        filename = f"thread_file_{i+1}{os.path.splitext(urlparse(url).path)[-1] or '.bin'}"
        t = threading.Thread(target=download_file, args=(url, filename))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    end = time.time()
    print(f"Concurrent download time: {end - start:.2f} seconds")
    return end - start


def main():
    print("Concurrent File Downloader")
    print("===========================")

    # ✅ Using dummy test-safe URLs that download small files
    urls = [
        "https://speed.hetzner.de/1MB.bin",
        "https://speed.hetzner.de/10MB.bin",
        "https://file-examples.com/wp-content/uploads/2017/10/file-example_PDF_1MB.pdf"
    ]

    print("\nUsing the following sample URLs:")
    for url in urls:
        print("-", url)

    
    seq_time = download_sequential(urls)

    
    thread_time = download_concurrent(urls)


    if thread_time > 0:
        speedup = seq_time / thread_time
    else:
        speedup = 0

    print("\nPerformance Summary:")
    print(f"- Sequential: {seq_time:.2f} seconds")
    print(f"- Concurrent: {thread_time:.2f} seconds")
    print(f"- Speedup:    {speedup:.2f}x")

if __name__ == "__main__":
    main()
