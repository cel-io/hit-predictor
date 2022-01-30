<template>
  <div>
    <b-tooltip
      :label="getFeatureDescription(feature)"
      type="is-primary is-light"
      multilined
      size="is-large"
    >
      <p class="is-size-4">{{ name }}</p></b-tooltip
    >
  </div>
</template>
<script>
import { getFeatureDescription } from "../helpers";

export default {
  props: {
    feature: {
      type: String,
      require: true,
    },
    name: {
      type: String,
      require: true,
    },
  },
  methods: {
    getFeatureDescription,
  },
};
</script>
