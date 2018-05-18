<template>
  <v-content>
    <v-layout>
      <v-flex xs12 sm6 offset-sm3>
        <v-card>
          <v-card-title primary-title>
              <h3 class="headline mb-0">Pryv</h3>
          </v-card-title>
          <v-card-text>
            <pre>{{streams}}</pre>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-content>
</template>

<script>
import auth from "@/auth";

export default {
  data() {
    return {
      streams: ""
    };
  },
  mounted() {
    this.getStreams();
  },
  methods: {
    getStreams() {
      var conn = auth.connection();
      var vm = this;

      var options = {
        state: null
      };
      conn.streams.get(options, function(err, streams) {
        var fstreams = streams.map(function(stream) {
          var obj = {
            name: stream.name
          };
          if (stream.children.length) {
            obj.children = stream._children.map(function(children) {
              return {
                name: children.name
              };
            });
          }
          return obj;
        });
        vm.streams = JSON.stringify(fstreams, null, 4);
      });
    }
  }
};
</script>
