<template>
  <form class="d-flex" method="get" action="/search/">
    <input list="autocompletes" class="form-control me-2" type="search"
           placeholder="Search vacancy, startup or CV"
           aria-label="Search" style="width: 500px" v-model="text" name="q"
           autocomplete="off" v-on="text.length > 2 ? {input: loadData} : {}">
    <datalist id="autocompletes">
      <option v-for="suggestion in data"
              :value="suggestion.autocomplete"></option>
    </datalist>
    &nbsp
    <button class="btn btn-success" type="submit">Search</button>
  </form>
</template>

<script>
export default {
  delimiters: ['[[', ']]'],
  data() {
    return {
      data: null,
      text: '',
    }
  },
  methods: {
    loadData() {
      fetch(`/api/v1/search/search-autocomplete/?q=${this.text}&limit=10`)
        .then(response => response.json())
        .then(data => this.data = data.results)
    },
  }
}
</script>
