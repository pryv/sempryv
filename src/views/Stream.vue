<template>
  <v-container>
      <v-toolbar
        :style="{ backgroundColor: clientDataColor(stream) }"
        dark>
        <v-toolbar-title>{{stream.name}}</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-toolbar-items>
          <v-btn
            v-if="stream.parentId"
            :to="{name:'stream', params:{id: stream.parentId}}"
            flat>
            <v-icon>arrow_upward</v-icon>&nbsp;{{ $t('Parent') }}
          </v-btn>
        </v-toolbar-items>
      </v-toolbar>
      <v-layout>
      </v-layout>
  </v-container>
</template>

<script>
import auth from "@/auth";

export default {
  props: ["value"],
  data() {
    return {
      stream: ""
    };
  },
  mounted() {
    this.getStream(this.$route.params.id);
  },
  beforeRouteUpdate(to, from, next) {
    this.getStream(to.params.id);
    next();
  },
  methods: {
    getStream(streamId) {
      var conn = auth.connection();
      var options = { id: streamId };
      var vm = this;
      conn.streams.update(options, function(err, streams) {
        vm.stream = streams;
      });
    },
    clientDataColor(stream) {
      if (stream.clientData) {
        if (stream.clientData["pryv-browser:bgColor"]) {
          return stream.clientData["pryv-browser:bgColor"];
        }
      }
      return "gray";
    }
  }
};
</script>
