OUT := ./out
PACKER_BUILD_ARM_IMAGE := mkaczanowski/packer-builder-arm
PACKER_BUILD_ARM_TAG := latest
PACKER_BUILD_ARM := $(PACKER_BUILD_ARM_IMAGE):$(PACKER_BUILD_ARM_TAG)

$(OUT)/:
	mkdir -p $@

$(OUT)/%.img: $(OUT)/%.pkr.json | $(OUT)/
	@docker run --rm --privileged -v /dev:/dev -v ${PWD}:/build $(PACKER_BUILD_ARM) build $<

$(OUT)/raspberry-pi-4.pkr.json: config/boards/raspberry-pi-4/ubuntu_server_20.04.pkr.json config/base.json | $(OUT)/
	@echo Building packer config $@ from $^
	@jq -s '.[0] * .[1] | .source.arm.ubuntu.image_path = "$(OUT)/$*.img"' $^ > $@

.PHONY: raspberry-pi-4
raspberry-pi-4: $(OUT)/raspberry-pi-4.img

.PHONY: all
all: raspberry-pi-4

clean:
	@rm -rf $(OUT)
