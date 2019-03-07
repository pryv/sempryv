<template>
  <div v-if="stream">
    <h2>{{ $t("Semantic annotations") }}</h2>
    <v-spacer />
    <v-layout wrap>
      <v-flex>
        <v-combobox v-model="selectedType" :items="types" label="Type" />
      </v-flex>
      <v-flex>
        <v-btn
          :disabled="!selectedType"
          color="primary"
          @click="addDialog = true"
          >Add</v-btn
        >
      </v-flex>
      <v-flex>
        <v-checkbox
          v-model="recursive"
          color="primary"
          label="Apply to children streams"
          @change="toggleRecursive()"
        />
      </v-flex>
    </v-layout>
    <template v-for="(items, type) in clienDataCodes()">
      <v-list :key="type">
        <v-subheader>{{ type }}</v-subheader>
        <template v-for="(item, index) in items">
          <v-list-tile :key="index">
            <v-list-tile-content>
              <v-list-tile-title>{{ item.display }}</v-list-tile-title>
              <v-list-tile-sub-title>
                <span class="system">{{ item.system_name }}</span> |
                {{ item.code }}
              </v-list-tile-sub-title>
            </v-list-tile-content>
            <v-list-tile-action @click="del(type, item)">
              <v-btn icon>
                <v-icon color="red lighten-1">delete</v-icon>
              </v-btn>
            </v-list-tile-action>
          </v-list-tile>
          <v-divider :key="index + 'divider'" :inset="item.inset" />
        </template>
      </v-list>
    </template>
    <v-dialog v-model="addDialog" persistent max-width="50%">
      <AddCode ref="addDialog" @close="addDialog = false" @add="add" />
    </v-dialog>
  </div>
</template>

<script>
import auth from "@/auth";
import semantic from "@/libraries/semantic";
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
      types: [],
      addDialog: false,
      recursive: false,
      selectedType: null
    };
  },
  watch: {
    value() {
      this.refresh();
    },
    addDialog(val) {
      if (val) this.$refs.addDialog.focus();
    }
  },
  mounted() {
    this.refresh();
  },
  methods: {
    clienDataCodes() {
      if (this.stream && this.stream.clientData && this.stream.clientData["sempryv:codes"]) {
          return this.stream.clientData["sempryv:codes"];
      }
      return null
    },
    refresh() {
      this.selectedType = null;
      this.getStream(this.value);
    },
    getStream(streamId) {
      var conn = auth.connection();
      var options = { id: streamId };
      var vm = this;
      conn.streams.getFlatenedObjects(options, function(err, streams) {
        vm.streams = streams;
        vm.stream = streams.filter(stream => {
          return stream.id == streamId;
        })[0];
        vm.recursive = semantic.get_recursive(vm.stream);
        semantic.get_event_types(vm.stream.id, function(types) {
          vm.types = types;
        });
      });
    },
    closeDialog() {
      this.addDialog = false;
    },
    add(item) {
      var vm = this;
      semantic.add_code(this.stream, this.selectedType, item, function(err) {
        if (err == null) {
          vm.closeDialog();
          vm.$emit("updated");
        }
      });
    },
    del(type, item) {
      var vm = this;
      semantic.del_code(this.stream, type, item, function(err) {
        if (err == null) {
          vm.$emit("updated");
          vm.refresh();
        }
      });
    },
    toggleRecursive() {
      var vm = this;
      semantic.set_recursive(this.stream, this.recursive, function() {
        vm.$emit("updated");
        vm.refresh();
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
