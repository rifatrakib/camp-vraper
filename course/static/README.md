## IMPORTANT!!!

This directory should contain `<spider-name>/headers.txt` and `<spider-name>/cookies.txt` which will be used to build corresponding `JSON` files in the same directory as the `txt` file. Store the headers necessary to make the requests from the spiders as text where each header follows `<header_name>=<header_value>` format and each such pairs are separated by `|` in between. For the cookies, they are stored as text as such each header follows `<cookie_name>=<cookie_value>` format and each such pairs are separated by `; `. The cookie can be directly copied from the `Developer Tools` of any browser.

For example, to run the `course_catalogue` spider, there should be a directory here named `course-catalogue` containing two plain text files with names `headers.txt` and `cookies.txt`. __Notice that the `_` from spider name was replaced with `-` in the directory name.__
