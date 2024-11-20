<template>
  <div class="profile-container">
    <!-- 상단 프로필 영역 -->
    <div class="profile-header">
      <div class="profile-img-container">
        <img src="@/views/accounts/img/profile.png" alt="Profile Image" class="profile-img" />
      </div>
      <div class="profile-info">
        <h3>UserName</h3>
        <p>010-1234-1123</p>
        <button class="contact-btn">회원정보 수정</button>
      </div>
    </div>

    
    <!-- 하단 Activity 영역 -->
    <div class="activity-section">
      <div class="activity-item">
        <h5>Reviews Written</h5>
        <p>15</p>
      </div>
      <div class="activity-item">
        <h5>Likes</h5>
        <p>120</p>
      </div>
      <div class="activity-item">
        <h5>Followers</h5>
        <p>300</p>
      </div>
    </div>
  </div>
<!-- 세부정보 -->
<div class="profile-details">

  <div class="profile-column">
    <h4>Reviews</h4>
  </div>

  <!-- ABOUT & SKILLS -->
  <div class="profile-column">
    <h4>MyMovie</h4>

  </div>
</div>
</template>

<script setup>
// 필요한 데이터 추가 (예: props, emits 등)
</script>

<style scoped src="./css/profile.css"></style>
