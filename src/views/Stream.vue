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
        <v-flex v-if="children.length != 0">
          <v-subheader>Childrens</v-subheader>
          <v-list dense>
            <v-list-tile
              v-for="child in children"
              :key="child.id"
              :to="{name:'stream', params:{id: child.id}}">
              <v-list-tile-title>{{ child.name }}</v-list-tile-title>
            </v-list-tile>
          </v-list>
        </v-flex>
      </v-layout>
  </v-container>
</template>

<script>
import auth from "@/auth";

export default {
  data() {
    return {
      stream: "",
      streams: []
    };
  },
  computed: {
    children() {
      if (!this.stream) {
        return [];
      }
      return this.stream.childrenIds.map(
        childrenId => this.streams.filter(stream => stream.id == childrenId)[0]
      );
    }
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
      conn.streams.getFlatenedObjects(options, function(err, streams) {
        vm.streams = streams;
        vm.stream = streams.filter(stream => {
          return stream.id == streamId;
        })[0];
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
