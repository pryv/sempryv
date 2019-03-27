<template>
  <v-card>
    <v-toolbar dark color="primary">
      <v-toolbar-title>{{ $t("Suggestions") }}</v-toolbar-title>
      <v-spacer />
      <v-btn icon dark @click.native="close()">
        <v-icon>close</v-icon>
      </v-btn>
    </v-toolbar>
    <v-card-text>
      <v-container fill-height fluid>
        <v-layout>
          <v-flex>
            <v-list>
              <template v-for="(item, index) in suggestions">
                <v-list-tile :key="index" @click="add(item)">
                  <v-list-tile-content>
                    <v-list-tile-title>{{ item.display }}</v-list-tile-title>
                    <v-list-tile-sub-title>
                      <span class="system">{{ item.system_name }}</span> |
                      {{ item.code }}
                    </v-list-tile-sub-title>
                  </v-list-tile-content>
                </v-list-tile>
                <v-divider :key="index + 'divider'" :inset="item.inset" />
              </template>
            </v-list>
            <div v-if="!suggestions || suggestions.len == 0">
              {{ $t("No suggestion") }}
            </div>
          </v-flex>
        </v-layout>
      </v-container>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: {
    kind: {
      type: String,
      default: ""
    },
    streamId: {
      type: String,
      default: ""
    }
  },
  data() {
    return {
      suggestions: []
    };
  },
  watch: {
    kind() {
      this.query(this.kind, this.streamId);
    },
    streamId() {
      this.query(this.kind, this.streamId);
    }
  },
  methods: {
    query(kind, streamId) {
      this.$http
        .get(
          process.env.VUE_APP_BACKEND +
            "/semantic/suggest?kind=" +
            kind +
            "&streamId=" +
            streamId
        )
        .then(response => {
          this.suggestions = response.body;
        });
    },
    close() {
      this.$emit("close");
    },
    add(item) {
      this.$emit("add", item);
    }
  }
};
</script>
