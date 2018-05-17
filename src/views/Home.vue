<template>
  <v-content>
    <v-layout>
      <v-flex xs12 sm6 offset-sm3>
        <v-card>
          <v-card-title primary-title>
              <h3 class="headline mb-0">Pryv</h3>
          </v-card-title>
          <v-card-text>
            {{streams}}
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

      conn.fetchStructure(function(err, streams) {
        vm.streams = String(streams);
      });
    }
  }
};
</script>
