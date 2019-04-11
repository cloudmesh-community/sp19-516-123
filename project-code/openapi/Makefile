UNAME := $(shell uname)
ifeq ($(UNAME), Darwin)
define terminal
  osascript -e 'tell application "Terminal" to do script "cd $(PWD); $1"'
endef
endif
ifeq ($(UNAME), Linux)
define terminal
  gnome-terminal --command 'bash -c "cd $(PWD); $1"'
endef
endif

install:
	pip install -r requirements.txt


put:
	$(call terminal, python server.py)
	sleep 3
	@echo "==============================================================================="
	@echo "Upload blobs"
	@echo "==============================================================================="
	curl -H "Content-Type:application/json" -X POST -d '{"service": "azureblob", "source": "~/sample/mp1.jpg", "destination": "/test", "recursive": "False"}' http://localhost:8080/cloudmesh/put_blob
	@echo
	@echo "==============================================================================="

list:
	$(call terminal, python server.py)
	sleep 3
	@echo "==============================================================================="
	@echo "list the blobs"
	@echo "==============================================================================="
	curl http://localhost:8080/cloudmesh/list_blob?service=azureblob'&'directory=%2ftest'&'recursive=True
	@echo
	@echo "==============================================================================="

search:
	$(call terminal, python server.py)
	sleep 3
	@echo "==============================================================================="
	@echo "search the blobs"
	@echo "==============================================================================="
	curl http://localhost:8080/cloudmesh/search_blob?service=azureblob'&'directory=%2ftest'&'filename=mp1%2ejpg'&'recursive=True
	@echo
	@echo "==============================================================================="

get:
	$(call terminal, python server.py)
	sleep 3
	@echo "==============================================================================="
	@echo "Get the blobs"
	@echo "==============================================================================="
	curl http://localhost:8080/cloudmesh/get_blob?service=azureblob'&'source=%7e%2fsample'&'destination=%2ftest%2fmp1%2ejpg'&'recursive=True
	@echo
	@echo "==============================================================================="

delete:
	$(call terminal, python server.py)
	sleep 3
	@echo "==============================================================================="
	@echo "delete the blobs"
	@echo "==============================================================================="
	curl http://localhost:8080/cloudmesh/delete_blob?service=azureblob'&'source=%2ftest%2fmp1%2ejpg'&'recursive=False
	@echo
	@echo "==============================================================================="

createdir:
	$(call terminal, python server.py)
	sleep 3
	@echo "==============================================================================="
	@echo "Create a Directory"
	@echo "==============================================================================="
	curl http://localhost:8080/cloudmesh/create_dir?service=azureblob'&'directory=%2fapi
	@echo
	@echo "==============================================================================="

