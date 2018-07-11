<template>
  <v-container
    v-if="stream">
    <v-layout
      row
      wrap>
      <v-flex xs12>
        <h2>{{ $t('Semantic annotations') }}</h2>
        <v-spacer/>
        <v-btn
          color="primary"
          @click="addDialog = true">
          Add
        </v-btn>
      </v-flex>
      <v-flex
        v-if="stream.clientData && stream.clientData.sempryv && stream.clientData.sempryv.codes"
        xs12>
        <v-list>
          <v-list-tile
            v-for="(item, index) in stream.clientData.sempryv.codes"
            :key="index">
            <v-list-tile-content>
              {{ item.display }}
            </v-list-tile-content>
            <v-list-tile-action @click="del(index)">
              <v-btn icon>
                <v-icon color="red lighten-1">delete</v-icon>
              </v-btn>
            </v-list-tile-action>
          </v-list-tile>
        </v-list>
      </v-flex>
    </v-layout>
    <v-dialog
      v-model="addDialog"
      persistent
      max-width="50%">
      <AddCode
        @close="addDialog = false"
        @add="add"/>
    </v-dialog>
  </v-container>
</template>

<script>
import auth from "@/auth";
import AddCode from "@/components/AddCode";

export default {
  components: {
    AddCode
  },
  props: {
    value: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      stream: null,
      addDialog: false
    };
  },
  watch: {
    value() {
      this.getStream(this.$route.params.id);
    }
  },
  mounted() {
    this.getStream(this.$route.params.id);
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
    closeDialog() {
      this.addDialog = false;
    },
    add(item) {
      if (!this.stream.clientData) {
        this.stream.clientData = {};
      }
      if (!this.stream.clientData.sempryv) {
        this.stream.clientData.sempryv = {};
      }
      if (!this.stream.clientData.sempryv.codes) {
        this.stream.clientData.sempryv.codes = [];
      }
      this.stream.clientData["sempryv"]["codes"].push(item);
      var conn = auth.connection();
      var vm = this;
      conn.streams.update(this.stream, function(err, streamUpdated) {
        if (err == null) {
          vm.closeDialog();
          vm.$emit("updated");
        }
      });
    },
    del(index) {
      this.stream.clientData.sempryv.codes.splice(index, 1);
      var conn = auth.connection();
      var vm = this;
      conn.streams.update(this.stream, function(err, streamUpdated) {
        if (err == null) {
          vm.$emit("updated");
        }
      });
    }
  }
};
</script>
