<template>
  <v-list>
    <div
      v-for="stream in value" :key="stream.name">
      <v-list-tile
        v-if="!stream.children"
        :to="{name:'stream', params:{name: stream.name}}">
        <v-list-tile-content>
          {{stream.name}}
        </v-list-tile-content>
      </v-list-tile>
      <v-list-group
        v-else>
        <v-list-tile
          slot="activator"
          :to="{name:'stream', params:{name: stream.name}}">
          <v-list-tile-content>
            C:{{stream.name}}
          </v-list-tile-content>
        </v-list-tile>
        <treeview
        v-model="stream.children"></treeview>
      </v-list-group>
    </div>
  </v-list>
</template>

<script>
export default {
  name: "treeview",
  props: ["value"],
  computed: {
    streams() {
      return JSON.stringify(this.value, null, 4);
    }
  }
};
</script>
