<template>
  <v-card>
    <v-toolbar
      dark
      color="primary">
      <v-toolbar-title>Add code</v-toolbar-title>
      <v-spacer/>
      <v-btn
        icon
        dark
        @click.native="$emit('close')">
        <v-icon>close</v-icon>
      </v-btn>
    </v-toolbar>
    <v-card-text>
      <v-container
        fill-height
        fluid>
        <v-layout>
          <v-flex>
            <h2>{{ $t('Semantic annotations') }}</h2>
            <v-text-field
              v-model="search"
              label="Semantic code"
              clearable
            />
            <div
              v-for="(item, index) in items"
              :key="index">
              <div>{{ item }}</div>
            </div>
          </v-flex>
        </v-layout>
      </v-container>
    </v-card-text>
    <v-card-actions>
      <v-spacer/>
      <v-btn
        color="primary"
        flat
        @click.stop="add()">Add</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      search: "",
      timer: null,
      items: []
    };
  },
  watch: {
    search() {
      if (self.timer != null) {
        clearTimeout(self.timer);
      }
      var vm = this;
      self.timer = setTimeout(function() {
        vm.query(vm.search);
      }, 200);
    }
  },
  methods: {
    query(val) {
      if (val == null || val == "") {
        this.items = [];
        return;
      }
      this.$http
        .get("http://localhost:8000/api/search?term=" + val)
        .then(response => {
          this.items = response.body.map(entry => entry.display);
        });
    }
  }
};
</script>
