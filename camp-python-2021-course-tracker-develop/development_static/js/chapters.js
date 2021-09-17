const Chapters = {
  delimiters: ['[[', ']]'],
  data() {
    return {
      chapter: [],
      id: undefined, // ID of current chapter.
    }
  },
  methods: {
    // Fetches filtered data by chapter id.
    loadData() {
      fetch(`/api/v1/courses/topics/?chapter=${this.id}`)
        .then(response => response.json())
        .then(data => this.chapter = data)
    },
    setId(id) {
      this.id = id
    }
  }
}

Vue.createApp(Chapters).mount('#chapters')
