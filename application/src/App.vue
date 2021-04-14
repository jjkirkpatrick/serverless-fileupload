<template>
  <v-app>
    <v-app-bar fixed app color="primary" dark>
      <div class="d-flex align-center">
        <v-btn
          href="http://jjkirk.com"
          target="_blank"
          text
          class="shrink mt-1 hidden-sm-and-down"
        >
          <span class="mr-2">FileUpload</span>
        </v-btn>
      </div>

      <v-spacer></v-spacer>

      <v-btn
        href="https://github.com/jjkirkpatrick/serverless-fileupload"
        target="_blank"
        text
      >
        <span class="mr-2">Github</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
//import HelloWorld from "./components/HelloWorld";

export default {
  name: "App",

  components: {
    //HelloWorld
  },

  data: () => ({
    //
  }),
};
</script>
