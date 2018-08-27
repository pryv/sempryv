<template>
  <v-card>
    <v-toolbar
      dark
      color="primary">
      <v-toolbar-title>{{ $t('Add code') }}</v-toolbar-title>
      <v-spacer/>
      <v-btn
        icon
        dark
        @click.native="close()">
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
              ref="search"
              v-model="search"
              :label="$t('Search')"
              clearable
            />
            <v-list>
              <v-divider/>
              <template v-for="(item, index) in items">
                <v-list-tile
                  :key="index"
                  @click="add(item)">
                  <v-list-tile-content>
                    <v-list-tile-title>{{ item.display }}</v-list-tile-title>
                    <v-list-tile-sub-title>
                      <span class="system">{{ item.system_name }}</span> | {{ item.code }}
                    </v-list-tile-sub-title>
                  </v-list-tile-content>
                </v-list-tile>
                <v-divider
                  :inset="item.inset"
                  :key="index + 'divider'"/>
              </template>
            </v-list>
          </v-flex>
        </v-layout>
      </v-container>
    </v-card-text>
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
    focus() {
      this.$nextTick(this.$refs.search.focus);
    },
    query(val) {
      if (val == null || val == "") {
        this.items = [];
        return;
      }
      this.$http
        .get(process.env.VUE_APP_BACKEND + "/api/search?term=" + val)
        .then(response => {
          this.items = response.body;
        });
    },
    reset() {
      clearTimeout(self.timer);
      this.search = "";
    },
    close() {
      this.reset();
      this.$emit("close");
    },
    add(item) {
      this.reset();
      this.$emit("add", item);
    }
  }
};
</script>
