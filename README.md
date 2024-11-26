# CineCode-PJT

## Daily 진행 상황
### 1117(일) 
>[민주]
>- [X] 피그마&컴포넌트 구조 작성 - 로그인, 회원가입
>
>[연지]
>- [x] ERD 설계

### 1118(월)
>[민주]
>- [X] 초기 영화, 장르 데이터 load
>- [X] 피그마&컴포넌트 구조 작성 - 홈
>
>[연지]
>- [X] 프로젝트 생성
>- [X] 로그인,회원가입 프론트

### 1119(화)
>[민주]
>- [ ] 홈 프론트
>- [ ] 홈 백엔드
>- [ ] 피그마&컴포넌트 구조도 작성 - 커뮤니티, 영화 상세 정보, 프로필
>
>[연지]
>- [X] 회원가입 백앤드
>- [X] ERD 수정

### 1120(수)
>[민주]
>- [X] 홈 프론트
>- [X] 홈 백엔드
>[연지]
>- [X] 로그인 구현, 
>- [X] 메인화면에 로그인된거 띄우기
>- 


### 1121(목)
>[민주]
>- [X] MovieDetail - 영화 정보, 예고편 프론트
>- [X] MovieDetail - 영화 정보, 예고편 백엔드
>- [X] fixtures 데이터 수정
>[연지]
>- [X] 회원정보 수정
>- [X] 프로필 프론트,백앤드
>- 

### 1122(금)
>[민주]
>- [ ] MovieDetail - 리뷰, 찜하기, 시청 상태 프론트
>- [ ] MovieDetail - 리뷰, 찜하기, 시청 상태 백엔드
>[연지]
>- [X] 음성 API 끌고 오기, 연결
>- [X] 프로필 사진 수정

---

## TIL
### 1123(토)
>[민주]
> #### router를 사용하면서 URL에 query를 표시하지 않는 방법
> HomeView.vue에서 SearchView.vue로 데이터를 전달할 때 2가지 방법이 존재
> 1. router의 params를 사용 <br>
> >1-1. 먼저 라우터 설정을 수정합니다:
> >```
> > {
> >  path: '/search/:searchData?',  // optional parameter
> >  name: 'Search',
> >  component: SearchView
> > }
> > ```
>
> > 1-2. HomeView.vue를 수정합니다:
> > ```
> > router.push({
> >     name: 'Search',
> >     params: {
> >       searchData: btoa(JSON.stringify(searchData)) // base64로 인코딩
>>     },
> >     replace: true // URL 히스토리를 남기지 않음
>>   });
>> ```
>
> > 1-3. SearchView.vue에서 params를 받아서 처리합니다:
> >```
> > onMounted(() => {
> >   if (route.params.searchData) {
> >     const searchData = JSON.parse(atob(route.params.searchData)); // base64 디코딩
> >     transcript.value = searchData.transcript;
> >     sentiment.value = searchData.sentiment;
> >     movies.value = searchData.movies;
> >   }
> > });
> > ```
>
> 2. router.push 시에 replace: true와 함께 query를 사용한 후, 즉시 query를 제거 <br>
> > 2-1. router 설정에 props: true 추가
> > ```
> > router.push({
> >    name: 'Search',
> >    query: {
> >      transcript: data.transcript,
> >      sentiment: data.sentiment_score,
> >      movies: JSON.stringify(data.movies)
> >    },
> >    replace: true
> >  }).then(() => {
> >     // query 제거
> >     router.replace({ name: 'Search' });
> >   });
> > ```
>
> 위의 방법을 사용하였던 데이터가 완전히 로드되기 전에 query가 제거되어 데이터가 사라지는 문제가 있었음.
> > 1. HomeView.vue는 기존 그대로 유지
> > 2. SearchView.vue에서 데이터를 로드한 후 URL을 정리합니다:
> > ```
> > onMounted(() => {
> >   // URL의 query params에서 데이터 가져오기
> >   const queryTranscript = route.query.transcript;
> >   const querySentiment = route.query.sentiment;
> >   const queryMovies = route.query.movies;
> >
> >   if (queryTranscript && querySentiment && queryMovies) {
> >     // 데이터 설정
> >     transcript.value = queryTranscript;
> >     sentiment.value = Number(querySentiment);
> >     movies.value = JSON.parse(queryMovies);
> >
> >     // 데이터 설정 후 URL 정리
> >     router.replace({ path: '/search' });
> >   }
> > });
> > ```
> 이렇게 하면:
> - SearchView가 마운트될 때 먼저 query 파라미터에서 데이터를 가져옵니다
> - 데이터를 컴포넌트의 상태로 설정합니다
> - 그 후에 URL을 깔끔하게 정리합니다
> - 이후 새로운 검색도 정상적으로 동작합니다
>
> 위의 방법대로 했는데 JSON 파싱 에러가 발생하여 claude-3.5-sonnet 모델을 활용한 cursor가 알려준 코드로 수정
> **쿼리 파라미터 처리 후 깨끗한 URL로 변경 (SearchView.vue onMounted 참고)**
>[연지]
>- [X] 음성인식 실시간으로 작성, 스크롤

### 1124(일)
>[민주]
>- [ ] MovieDetail - 리뷰, 찜하기, 시청 상태 프론트
>- [ ] MovieDetail - 리뷰, 찜하기, 시청 상태 백엔드
>[연지]
>- [X] 음성인식 오류 해결
>- [X] 프로필 페이지 css 수정

### 1125(월)
>[민주]
>- [ ] 
>- [ ] 
>[연지]
>- [X] 검색창 작업
>- [X] 검색창 css 작업


### 1126(화)
>[민주]
>- [ ] 
>- [ ] 
>[연지]
>- [X] PPT 작업
>- [X] 영화 url 작업


### 1127(수)
>[민주]
>- [ ] 
>- [ ] 
>[연지]
>- [X] PPT 작업
>- [X] 리뷰,프로필 css 작업
>- [X] Navbar 시계 추가



---

## 시간 남으면 추가 할 거

- [ ] 로그인 할 때 회원가입 안 된 계정 에러 메시지 띄우기
- [ ] 사용자 ID랑 Email 바꾸기
- [ ] 소셜 로그인
