<template>
  <v-container 
    v-if="stream" 
    fill-height 
    fluid>
    <v-layout>
      <v-flex>
        <h2>{{ $t('Semantic annotations') }}</h2>
        <p>{{ stream.id }}</p>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import auth from "@/auth";

export default {
  props: {
    value: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      stream: null
    };
  },
  watch: {
    value() {
      this.getStream(this.$route.params.id);
    }
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
    }
  }
};
</script>
