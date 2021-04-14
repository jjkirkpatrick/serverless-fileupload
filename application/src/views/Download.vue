<template>
  <v-main>
    <v-container class="fill-height" fluid>
      <v-row align="center" justify="center">
        <v-col cols="12" sm="8" md="4">
          <v-card class="elevation-12">
            <v-toolbar color="grey" dark flat>
              <v-toolbar-title>File download</v-toolbar-title>
            </v-toolbar>

            <v-divider></v-divider>

            <v-row class="ma-3" justify="center" no-gutters>
              <v-col md="6" v-if="file == 404 && file != null"
                >The file you reqested does not exist!</v-col
              >
              <v-col v-else-if="file !== 404 && file != null">
                <div>
                  <b>File Name:</b>
                  {{ file.filename }}
                </div>
                <div>
                  <b>File Size:</b>
                  {{ readableSize }}
                </div>
              </v-col>
              <v-col md="6" class="text-center" v-else>
                <v-progress-circular
                  :size="70"
                  :width="7"
                  color="purple"
                  indeterminate
                ></v-progress-circular>
              </v-col>
            </v-row>
            <v-divider></v-divider>

            <v-row class="ma-3" justify="center" no-gutters>
              <v-col md="6">
                <v-btn
                  @click="download"
                  block
                  tile
                  color="indigo"
                  dark
                  :disabled="file == 404 || disableDownload == true"
                  >Download</v-btn
                >
              </v-col>
            </v-row>

            <v-divider></v-divider>
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
  </v-main>
</template>


<script>
export default {
  data() {
    return {
      file: null,
      disableDownload: null,
      error: null,
    };
  },
  computed: {
    readableSize() {
      return this.formatBytes(this.file.filesize);
    },
  },
  methods: {
    // human readable file size lifted from https://codepen.io/amontagu/pen/MXwjBb
    formatBytes(a, b) {
      if (0 == a) return "0 Bytes";
      var c = 1024,
        d = b || 2,
        e = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"],
        f = Math.floor(Math.log(a) / Math.log(c));
      return parseFloat((a / Math.pow(c, f)).toFixed(d)) + " " + e[f];
    },
    init() {
      this.$http
        .get("https://api.jjkirk.com/get/" + this.$route.params.download)
        .then((result) => {
          console.log(result.data);
          this.file = JSON.parse(result.data.body);
        })
        .catch((result) => {
          this.error = result;
          this.file = 404;
        });
    },
    download() {
      window.open(this.file.key, "_blank");
      this.disableDownload = true;
    },
  },
  mounted() {
    this.init();
  },
};
</script>


