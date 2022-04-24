<template>
  <div>
    <div v-if="isFetching">Loading...</div>

    <div
      v-if="articles"
      class="p-2 grid lg:grid-cols-2 gap-20 my-10 container mx-auto"
    >
      <article
        class="grid mx-auto group transition-all duration-700 ease-out hover:cursor-pointer"
        v-for="(article, index) in articles"
        :key="'article-' + index"
      >
        <img
          class="group-hover:contrast-150 transition-all duration-1000 ease-out w-full aspect-video rounded-xl md:rounded-3xl"
          :src="`${publicPath}felipe-simo-T-U6wuM0lvg-unsplash.jpg`"
          alt="abstract"
        />
        <h2
          class="group-hover:text-zinc-700 mt-3 ease-out transition-all duration-6000 text-3xl lg:text-4xl font-letter"
        >
          {{ article.name }}
        </h2>
        <div
          class="group-hover:text-zinc-600 ease-out transition-all flex flex-wrap items-center"
        >
          <div
            class="my-2 last:mr-6 mr-3 p-2 border border-black rounded"
            v-for="(tag, index) in article.tags"
            :key="'tag-' + index"
          >
            {{ tag.name }}
          </div>
          <time
            :datetime="article.createdAt"
            class="py-4 text-stone-500 text-lg"
          >
            Ajouté le {{ getLocalDate(article.createdAt) }}</time
          >
        </div>
        <div
          class="text-justify group-hover:text-zinc-600 ease-out transition-all sm:mt-3 text-stone-700 text-lg tracking-wide leading"
        >
          {{ article.teaser }}
        </div>
      </article>
    </div>
  </div>
</template>

<script lang="ts" setup>
  import { computed, Ref } from '@vue/runtime-dom'
  import format from 'date-fns/format/index.js'
  import { useQuery } from 'villus'
  import { gql } from 'graphql-tag'

  interface Author {
    id: number
    auth0Id: string
    email: string
    username: string
    isAdmin: boolean
    articles: Article[]
  }

  interface Tag {
    name: string
  }

  interface Article {
    id: number
    name: string
    teaser: string
    body: string
    author: Author
    tags: Tag[]
    createdAt: string
    modifiedAt: string
    url: string
    readingTime: string
  }

  const { data, isFetching } = useQuery({
    query: gql`
      query GetArticles {
        articles {
          id
          name
          createdAt
          teaser
          tags {
            name
          }
        }
      }
    `,
  })
  const articles: Ref<Article[]> = computed(() => {
    return data.value?.articles || []
  })

  const publicPath = '/public/img/'

  /**
   * Get the locale date and return a nice date format.
   */
  const getLocalDate = (simpleDate: string | Date): string => {
    const date = new Date(simpleDate)
    return format(date, 'dd-MM-yyyy')
  }
</script>
