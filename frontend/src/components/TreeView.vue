<template>
  <v-list>
    <div
      v-for="stream in value"
      :style="{ paddingLeft: indentation }" 
      :key="stream.name">
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
          {{ stream.name }}
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
              :style="{ color: clientDataColor(stream) }"
              size="18"
              left>
              mdi-checkbox-multiple-blank-circle
            </v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            {{ stream.name }}
          </v-list-tile-content>
        </v-list-tile>
        <treeview
          v-model="stream.children"
          :level="level + 1"/>
      </v-list-group>
    </div>
  </v-list>
</template>

<script>
export default {
  name: "Treeview",
  props: {
    value: {
      type: Array,
      required: true
    },
    level: {
      type: Number,
      required: true
    }
  },
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
