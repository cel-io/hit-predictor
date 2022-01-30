<template>
  <div class="box has-text-centered">
    <b-tooltip
      :label="getFeatureDescription(feature)"
      type="is-primary is-light"
      multilined
      size="is-large"
    >
      <p class="is-size-4">{{ name }}</p></b-tooltip
    >
    <p class="is-size-5">
      {{ value }}
    </p>
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
    value: {
      require: true,
    },
  },
  methods: {
    getFeatureDescription,
  },
};
</script>
