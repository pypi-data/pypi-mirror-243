LAVA_IMAGE ?= ""
RUNTIME ?= "podman"

aemva_version ?= "11.23_9"
aemva_version_sha256 ?= "9d43c8eb347bf169a024cdbbc04572d169f60098fe061316b36bdbd4a44ffd79"
morello_version ?= "0.11_34"
morello_version_sha256 ?= "ed1e110fb7fa8732d4f1bea9af69491a9e3f7dbf57d2ce6ea916d3cdf910d324"

container_aemva_version = $(shell echo $(aemva_version)|sed -e 's|_|.|g')
container_morello_version = $(shell echo $(morello_version)|sed -e 's|_|.|g')

.PHONE: build

build: fvp-aemva fvp-morello

fvp-aemva: aemva/Dockerfile
	cd aemva && $(RUNTIME) build --build-arg version=$(aemva_version) --build-arg version_sha256=$(aemva_version_sha256) --tag fvp:aemva-$(container_aemva_version) .

fvp-morello: morello/Dockerfile
	cd morello && $(RUNTIME) build --build-arg version=$(morello_version) --build-arg version_sha256=$(morello_version_sha256) --tag fvp:morello-$(container_morello_version) .

clean:
	$(RUNTIME) image rm fvp:aemva-$(container_aemva_version) fvp:morello-$(container_morello_version)
