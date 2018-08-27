<template>
  <v-container
    v-if="object">
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
        v-if="object.clientData && object.clientData.sempryv && object.clientData.sempryv.codes"
        xs12>
        <v-list>
          <v-divider/>
          <template v-for="(item, index) in object.clientData.sempryv.codes">
            <v-list-tile :key="index">
              <v-list-tile-content>
                <v-list-tile-title>{{ item.display }}</v-list-tile-title>
                <v-list-tile-sub-title>
                  <span class="system">{{ item.system_name }}</span> | {{ item.code }}
                </v-list-tile-sub-title>
              </v-list-tile-content>
              <v-list-tile-action @click="del(index)">
                <v-btn icon>
                  <v-icon color="red lighten-1">delete</v-icon>
                </v-btn>
              </v-list-tile-action>
            </v-list-tile>
            <v-divider
              :inset="item.inset"
              :key="index + 'divider'"/>
          </template>
        </v-list>
      </v-flex>
    </v-layout>
    <v-dialog
      v-model="addDialog"
      persistent
      max-width="50%">
      <AddCode
        ref="addDialog"
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
    },
    type: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      object: null,
      addDialog: false
    };
  },
  watch: {
    value() {
      this.getObject(this.$route.params.id);
    },
    addDialog(val) {
      if (val) this.$refs.addDialog.focus();
    }
  },
  mounted() {
    this.getObject(this.$route.params.id);
  },
  methods: {
    getObject(objectId) {
      if (this.type == "stream") {
        return this.getStream(objectId);
      } else if (this.type == "event") {
        return this.getEvent(objectId);
      }
    },
    getStream(streamId) {
      var conn = auth.connection();
      var options = { id: streamId };
      var vm = this;
      conn.streams.getFlatenedObjects(options, function(err, streams) {
        vm.streams = streams;
        vm.object = streams.filter(stream => {
          return stream.id == streamId;
        })[0];
      });
    },
    getEvent(eventId) {
      var conn = auth.connection();
      var filter = {};
      var vm = this;
      conn.events.get(filter, function(err, events) {
        vm.object = events.filter(event => {
          return event.id == eventId;
        })[0];
      });
    },
    closeDialog() {
      this.addDialog = false;
    },
    add(item) {
      if (!this.object.clientData) {
        this.object.clientData = {};
      }
      if (!this.object.clientData.sempryv) {
        this.object.clientData.sempryv = {};
      }
      if (!this.object.clientData.sempryv.codes) {
        this.object.clientData.sempryv.codes = [];
      }
      this.object.clientData["sempryv"]["codes"].push(item);
      if (this.type == "stream") {
        return this.updateStream();
      } else if (this.type == "event") {
        return this.updateEvent();
      }
    },
    updateStream() {
      var conn = auth.connection();
      var vm = this;
      conn.streams.update(this.object, function(err) {
        if (err == null) {
          vm.closeDialog();
          vm.$emit("updated");
        }
      });
    },
    updateEvent() {
      var conn = auth.connection();
      var vm = this;
      conn.events.update(this.object, function(err) {
        if (err == null) {
          vm.closeDialog();
          vm.$emit("updated");
        }
      });
    },
    del(index) {
      this.object.clientData.sempryv.codes.splice(index, 1);
      if (this.type == "stream") {
        return this.delFromStream();
      } else if (this.type == "event") {
        return this.delFromEvent();
      }
    },
    delFromStream() {
      var conn = auth.connection();
      var vm = this;
      conn.streams.update(this.object, function(err) {
        if (err == null) {
          vm.$emit("updated");
        }
      });
    },
    delFromEvent() {
      var conn = auth.connection();
      var vm = this;
      conn.events.update(this.object, function(err) {
        if (err == null) {
          vm.$emit("updated");
        }
      });
    }
  }
};
</script>

<style>
.system {
  color: lightseagreen;
}
</style>
