<script>
/* eslint-disable  no-unused-vars */
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 1;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}

.madeBy {
  font-size: 10px;
}
</style>>

<template>
  <v-content>
    <v-container class="fill-height" fluid>
      <v-row align="center" justify="center">
        <v-col cols="12" sm="8" md="4">
          <v-card :loading="uploading" class="elevation-12">
            <v-toolbar color="grey" dark flat>
              <v-toolbar-title>test File Upload</v-toolbar-title>
            </v-toolbar>

            <v-divider></v-divider>

            <v-row class justify="center" no-gutters>
              <v-col class="ma-5" md="6">
                <div>
                  <p class="text-center font-weight-thin">Select your file!</p>
                </div>
                <v-flex xs12 sm12 d-flex>
                  <v-file-input
                    @change="resetUi"
                    v-model="files"
                    placeholder="Click here to select your file"
                  />
                </v-flex>
              </v-col>
            </v-row>

            <v-row class justify="center" no-gutters>
              <v-col md="6">
                <div>
                  <p class="text-center font-weight-thin">
                    How long before your file is deleted?
                  </p>
                </div>
                <v-flex class="mb-5" xs12 sm12 d-flex>
                  <v-select
                    v-model="select"
                    :hint="`${select.abbr}`"
                    :items="items"
                    item-text="state"
                    item-value="abbr"
                    label="Select"
                    persistent-hint
                    return-object
                    single-line
                  ></v-select>
                </v-flex>
              </v-col>
            </v-row>
            <v-divider></v-divider>

            <v-row class="ma-3" justify="center" no-gutters>
              <v-col md="6">
                <v-btn @click="upload" block tile color="indigo" dark
                  >Upload</v-btn
                >
              </v-col>
            </v-row>

            <v-divider></v-divider>
            <v-card-actions>
              <transition name="fade">
                <v-alert
                  width="100%"
                  v-if="uploading && !downloadlink"
                  border="left"
                  color="indigo"
                  dark
                >
                  <p class="text-center ma-0">
                    Please wait whilst your file uploads
                    <v-progress-circular
                      :size="70"
                      :width="7"
                      color="primary"
                      :value="uploadPercentage"
                      :rotate="-90"
                      >{{ uploadPercentage }}%</v-progress-circular
                    >
                  </p>
                </v-alert>
              </transition>
            </v-card-actions>
            <v-card-actions>
              <transition name="fade">
                <v-alert
                  width="100%"
                  v-if="downloadlink"
                  border="left"
                  color="success"
                  dark
                >
                  <p class="text-center ma-0">
                    Your download link is :
                    <a :href="downloadlink">{{ downloadlink }}</a>
                  </p>
                </v-alert>
              </transition>
            </v-card-actions>
          </v-card>
          <v-col
            cols="12"
            class="madeBy font-weight-thin text--disabled text-right"
          >
            Made with
            <v-icon size="10" color="red" dense>fa-heart</v-icon>by Joshua
            Kirkpatrick
          </v-col>
        </v-col>
      </v-row>
    </v-container>
  </v-content>
</template>


<script>
export default {
  data() {
    return {
      files: null,
      uploading: false,
      downloadlink: null,
      uploadPercentage: null,
      uploadTotalSize: null,
      select: {
        state: "Delete after download",
        abbr: "File will be deleted after the first download",
        id: 1,
      },
      items: [
        {
          state: "Delete After Download",
          abbr: "File will be deleted after the first download",
          id: 1,
        },
        {
          state: "30 Minuets",
          abbr: "File will be deleted after 30 minuets",
          id: 2,
        },
        { state: "1 Hour", abbr: "File will be deleted in 1 hour", id: 2 },
        { state: "1 Day", abbr: "File will be deleted in 1 day", id: 3 },
        { state: "1 Week", abbr: "File will be deleted in 1 week", id: 4 },
      ],
    };
  },
  props: {
    source: String,
  },
  methods: {
    generateFormData(data, file) {
      const formData = new FormData();
      formData.append("key", data.key);
      formData.append("x-amz-algorithm", data["x-amz-algorithm"]);
      formData.append("x-amz-credential", data["x-amz-credential"]);
      formData.append("x-amz-date", data["x-amz-date"]);
      formData.append("x-amz-security-token", data["x-amz-security-token"]);
      formData.append("policy", data["policy"]);
      formData.append("x-amz-signature", data["x-amz-signature"]);
      formData.append("file", file);
      formData.append("Content-Type", this.files.type);
      return formData;
    },
    resetUi() {
      this.uploading = false;
      this.downloadlink = null;
      this.uploadPercentage = null;
      this.uploadTotalSize = null;
    },
    upload(e) {
      if (this.files) {
        var path =
          "https://api.jjkirk.com/presignpost?filename=" +
          this.files.name +
          "&filetype=" +
          e.type +
          "&expiry=" +
          this.select.id +
          "&filesize=" +
          this.files.size;
        this.$http.get(path).then((result) => {
          var formData = this.generateFormData(
            JSON.parse(result.data.body).key.fields,
            this.files
          );
          this.downloadlink = null;
          this.uploading = true;
          this.$http
            .post(JSON.parse(result.data.body).key.url, formData, {
              onUploadProgress: function (progressEvent) {
                this.uploadPercentage = Math.round(
                  (progressEvent.loaded / progressEvent.total) * 100
                );
              }.bind(this),
            })
            .then((response) => {
              this.uploading = false;
              this.downloadlink =
                "http://jjkirk.com/#/" +
                JSON.parse(result.data.body).downloadlink;
            });
        });
      } else {
        this.uploading = false;
        this.downloadlink = null;
      }
    },
  },
};
</script>
