<script setup>
import DefaultTheme from 'vitepress/theme'
import PageSlidesButton from './components/PageSlidesButton.vue'
</script>

<template>
  <DefaultTheme.Layout>
    <template #nav-bar-content-after>
      <ClientOnly>
        <PageSlidesButton />
      </ClientOnly>
    </template>
  </DefaultTheme.Layout>
</template>
