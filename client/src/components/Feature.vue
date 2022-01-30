<template>
  <div class="box has-text-centered">
    <feature-title :feature="feature" :name="name" />
    <p class="is-size-5">
      {{ value }}
    </p>
  </div>
</template>
<script>
import FeatureTitle from "./FeatureTitle.vue";

export default {
  components: {
    FeatureTitle,
  },
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
};
</script>
