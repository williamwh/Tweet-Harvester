docker service create -e HTTPS_PROXY=http://wwwproxy.unimelb.edu.au:8000/ --name standard_search1 williamhe9/my_repo:standard_search 0 covid
docker service create -e HTTPS_PROXY=http://wwwproxy.unimelb.edu.au:8000/ --name standard_search2 williamhe9/my_repo:standard_search 1 corona
docker service create -e HTTPS_PROXY=http://wwwproxy.unimelb.edu.au:8000/ --name standard_search3 williamhe9/my_repo:standard_search 2 iso
docker service create -e HTTPS_PROXY=http://wwwproxy.unimelb.edu.au:8000/ --name standard_search4 williamhe9/my_repo:standard_search 3 ""
docker service create -e HTTPS_PROXY=http://wwwproxy.unimelb.edu.au:8000/ --name stream_search1 williamhe9/my_repo:stream_search 0
docker service create -e HTTPS_PROXY=http://wwwproxy.unimelb.edu.au:8000/ --name stream_search2 williamhe9/my_repo:stream_search 1
docker service create -e HTTPS_PROXY=http://wwwproxy.unimelb.edu.au:8000/ --name stream_search3 williamhe9/my_repo:stream_search 2
docker service create -e HTTPS_PROXY=http://wwwproxy.unimelb.edu.au:8000/ --name stream_search4 williamhe9/my_repo:stream_search 3