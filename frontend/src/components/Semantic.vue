<template>
  <div v-if="stream">
    <h2>{{ $t('Semantic annotations') }}</h2>
    <v-spacer/>
    <v-btn
      color="primary"
      @click="addDialog = true">
      Add
    </v-btn>
    <template
      v-for="(items, type) in stream.clientData['sempryv:codes']">
      <v-list :key="type">
        <v-subheader>{{ type }}</v-subheader>
        <template v-for="(item, index) in items">
          <v-list-tile :key="index">
            <v-list-tile-content>
              <v-list-tile-title>{{ item.display }}</v-list-tile-title>
              <v-list-tile-sub-title>
                <span class="system">{{ item.system_name }}</span> | {{ item.code }}
              </v-list-tile-sub-title>
            </v-list-tile-content>
            <v-list-tile-action @click="del(item)">
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
    </template>
    <v-dialog
      v-model="addDialog"
      persistent
      max-width="50%">
      <AddCode
        ref="addDialog"
        @close="addDialog = false"
        @add="add"/>
    </v-dialog>
  </div>
</template>

<script>
import auth from "@/auth";
import { add_code, del_code } from "@/libraries/semantic";
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
    refresh() {
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
      });
    },
    closeDialog() {
      this.addDialog = false;
    },
    add(item) {
      var vm = this;
      add_code(this.stream, "note/txt", item, function(err) {
        if (err == null) {
          vm.closeDialog();
          vm.$emit("updated");
        }
      });
    },
    del(item) {
      var vm = this;
      del_code(this.stream, "note/txt", item, function(err) {
        if (err == null) {
          vm.$emit("updated");
          vm.refresh();
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
