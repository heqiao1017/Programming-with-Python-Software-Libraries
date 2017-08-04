# download_file.py
#
# ICS 32 Fall 2016
# Code Example
#
# This is a short program that demonstrates how to download the contents
# of a URL from the web and save it into a file on the local hard drive.
# The program doesn't attempt to do anything interesting with the file;
# it saves whatever the web server sends back into the file, without
# regard to what it is, formatting concerns, or anything else; it is
# what it is.
#
# One thing that appears here that does not appear in the write-up
# accompanying this example is the use of the urllib.error.HTTPError
# exception, which is raised by urllib.request.urlopen() whenever an
# attempt to download a web page fails (e.g., because you try to
# download a page that does not exist).  When that exception is raised,
# you can catch it and use its code attribute to determine what status
# code the server returned (e.g., 404 means that the page was not found,
# i.e., that it doesn't exist).

import http.client
import urllib.request
import urllib.error


def user_interface() -> None:
    url = _choose_url()

    if len(url) == 0:
        return
    else:
        print()
        save_path = _choose_save_path()

        if len(save_path) == 0:
            return
        else:
            _download_url(url, save_path)



def _choose_url() -> str:
    print('Choose a URL to download (press Enter or Return to quit)')
    return input('URL: ').strip()



def _choose_save_path() -> str:
    print('Choose where you\'d like to save the file you download')
    return input('Path: ').strip()



def _download_url(url_to_download: str, file_path: str) -> None:
    response = None
    file_to_save = None

    try:
        response = urllib.request.urlopen(url_to_download)
        file_to_save = open(file_path, 'wb')
        file_to_save.write(response.read())

    except urllib.error.HTTPError as e:
        print('Failed to download contents of URL')
        print('Status code: {}'.format(e.code))
        print()

    finally:
        if file_to_save != None:
            file_to_save.close()
        
        if response != None:
            response.close()



if __name__ == '__main__':
    user_interface()
