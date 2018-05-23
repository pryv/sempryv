<template>
  <v-list>
    <div
      :style="{ paddingLeft: indentation }"
      v-for="stream in value" :key="stream.name">
      <v-list-tile
        v-if="stream.children.length == 0"
        :to="{name:'stream', params:{id: stream.id}}">
        <v-list-tile-action>
          <v-icon
            :style="{ color: clientDataColor(stream) }"
            left>
            fa-circle
          </v-icon>
        </v-list-tile-action>
        <v-list-tile-content>
          {{stream.name}}
        </v-list-tile-content>
      </v-list-tile>
      <v-list-group
        v-else>
        <v-list-tile
          slot="activator"
          :to="{name:'stream', params:{id: stream.id}}"
          @click.native.stop>
          <v-list-tile-action>
            <v-icon
              size="18"
              :style="{ color: clientDataColor(stream) }"
              left>
              mdi-checkbox-multiple-blank-circle
            </v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            {{stream.name}}
          </v-list-tile-content>
        </v-list-tile>
        <treeview
        v-model="stream.children"
        :level="level + 1"></treeview>
      </v-list-group>
    </div>
  </v-list>
</template>

<script>
export default {
  name: "treeview",
  props: ["value", "level"],
  computed: {
    indentation() {
      return this.level * 10 + "px";
    }
  },
  methods: {
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
