<template>
  <v-app>
    <!-- ✅ 상단 네비게이션 바 -->
    <v-app-bar app color="white" elevation="1">
      <v-toolbar-title class="text-black font-weight-bold">
        <v-img :src="logo" alt="NewsPick Logo" height="100" width="100" class="mr-2" />
      </v-toolbar-title>

      <v-spacer></v-spacer>

      <v-row no-gutters align="center" class="mr-4" style="max-width: 350px">
        <v-col>
          <v-text-field
            v-model="searchQuery"
            hide-details
            solo
            flat
            placeholder="뉴스 검색"
            prepend-inner-icon="mdi-magnify"
            density="compact"
            class="text-black"
          ></v-text-field>
        </v-col>
        <v-col cols="auto">
          <v-btn color="black" variant="flat" @click="search">검색</v-btn>
        </v-col>
      </v-row>

      <v-btn variant="text" class="text-black">로그인</v-btn>
      <v-btn variant="text" class="text-black">대시보드</v-btn>
    </v-app-bar>

    <!-- ✅ 메인 콘텐츠 영역 -->
    <v-main>
      <v-container class="mt-8" style="max-width: 1000px" fluid>
        <v-row dense>
          <v-col cols="12" md="6">
            <v-card class="pa-4" outlined>
              <v-card-title>📌 오늘의 뉴스</v-card-title>
              <v-card-text>주요 뉴스를 요약해서 보여줍니다.</v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="6">
            <v-card class="pa-4" outlined>
              <v-card-title>🗝️ 일간 뉴스 키워드</v-card-title>
              <v-card-text>오늘의 키워드를 분석해서 보여줍니다.</v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="6">
            <v-card class="pa-4" outlined>
              <v-card-title>📆 주간 뉴스</v-card-title>
              <v-card-text>이번 주 가장 많이 읽힌 뉴스입니다.</v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="6">
            <v-card class="pa-4" outlined>
              <v-card-title>🧠 주간 뉴스 키워드</v-card-title>
              <v-card-text>한 주간 뉴스에서 추출한 핵심 키워드입니다.</v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12">
            <v-card class="pa-4" outlined>
              <v-card-title>📰 최신 뉴스 모음</v-card-title>
              <v-card-text>방금 등록된 최신 뉴스 목록입니다.</v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'
import logo from '@/assets/NewsPick.svg'


const searchQuery = ref('')

function search() {
  console.log('검색어:', searchQuery.value)
}
</script>
