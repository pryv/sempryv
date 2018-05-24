<template>
  <v-container fluid>
    <v-card>
      <v-toolbar
        :style="{ backgroundColor: clientDataColor(stream) }"
        dark>
        <v-toolbar-title>{{stream.name}}</v-toolbar-title>
      </v-toolbar>
      <v-container fluid grid-list-xs>
        <v-layout row wrap>
          <v-flex d-flex xs9>
          </v-flex>
          <v-flex
            d-flex
            xs3
            style="border-left: solid 1px gray;">
            <v-list dense>
              <v-subheader>{{ $t('Navigation') }}</v-subheader>
              <v-list-tile
                v-if="parent"
                :to="{name:'stream', params:{id: parent.id}}">
                <v-list-tile-action>
                  <v-icon>arrow_upward</v-icon>
                </v-list-tile-action>
                <v-list-tile-content>
                  {{parent.id}}
                </v-list-tile-content>
              </v-list-tile>
              <v-divider v-if="parent && children.length > 0"></v-divider>
              <v-list-tile
                v-for="child in children"
                :key="child.id"
                :to="{name:'stream', params:{id: child.id}}">
                <v-list-tile-action>
                  <v-icon>subdirectory_arrow_right</v-icon>
                </v-list-tile-action>
                <v-list-tile-content>{{ child.name }}</v-list-tile-content>
              </v-list-tile>
              <v-subheader>{{ $t('Stream info') }}</v-subheader>
              <v-list-tile>
                <v-list-tile-title>
                  {{ $t('Id') }}
                </v-list-tile-title>
                <v-list-tile-sub-title>
                  {{ stream.id }}
                </v-list-tile-sub-title>
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-title>
                  {{ $t('Name') }}
                </v-list-tile-title>
                <v-list-tile-sub-title>
                  {{ stream.name }}
                </v-list-tile-sub-title>
              </v-list-tile>
            </v-list>
          </v-flex>
        </v-layout>
      </v-container>
    </v-card>
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
    },
    parent() {
      if ((!this.stream) || (!this.stream.parentId)) {
        return null;
      }
      console.log(this.streams.filter(stream => stream.id == this.stream.parentId)[0])
      return this.streams.filter(stream => stream.id == this.stream.parentId)[0]
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
