<template>
  <div class="flex flex-col bg-white w-full m-8 p-8 rounded-3xl shadow-xl max-w-4xl mx-auto">
    <!-- Заголовок страницы "О нас" -->
    <div class="mb-10 text-center">
      <h1 class="text-3xl text-slate-600 uppercase border-b-2 pb-4 mb-6">About Our Service</h1>
      <p class="text-lg text-slate-500 mx-auto">
        We are a photography aggregator platform connecting talented photographers with customers
        who are looking for the perfect photoshoot experience.
      </p>
    </div>

    <!-- Описание компании -->
    <section class="mb-10">
      <h2 class="text-3xl font-semibold text-slate-700 mb-4">About the Company</h2>
      <p class="text-slate-600 leading-relaxed">
        We are committed to providing easy access to professional photographers who can capture
        your most precious moments. Whether it’s a wedding, family portrait, or an event, we have
        the perfect photographer for you. Our goal is to simplify the process of booking the best
        photographers available and to help you find the perfect match for your photoshoot needs.
      </p>
    </section>

    <!-- Миссия -->
    <section class="mb-10 bg-gradient-to-r from-orange-100 via-orange-50 to-orange-200 p-6 rounded-xl shadow-lg">
      <h2 class="text-3xl font-semibold text-slate-700 mb-4">Our Mission</h2>
      <p class="text-slate-600 leading-relaxed">
        Our mission is to democratize access to high-quality photography services and make the booking
        process easier and faster for everyone. We strive to create a platform where photographers and
        clients can come together seamlessly, and where creativity thrives.
      </p>
    </section>

    <!-- Преимущества -->
    <section class="mb-10">
      <h2 class="text-3xl font-semibold text-slate-700 mb-4">Why Choose Us?</h2>
      <ul class="list-disc pl-5 space-y-3 text-slate-600">
        <li class="flex items-center">
          <span class="w-2.5 h-2.5 bg-orange-600 rounded-full mr-3"></span>
          Wide variety of professional photographers to choose from
        </li>
        <li class="flex items-center">
          <span class="w-2.5 h-2.5 bg-orange-600 rounded-full mr-3"></span>
          Competitive pricing for all types of photoshoots
        </li>
        <li class="flex items-center">
          <span class="w-2.5 h-2.5 bg-orange-600 rounded-full mr-3"></span>
          Easy-to-use platform for booking photographers
        </li>
        <li class="flex items-center">
          <span class="w-2.5 h-2.5 bg-orange-600 rounded-full mr-3"></span>
          Reliable customer support to help with any inquiries
        </li>
      </ul>
    </section>

    <!-- Контакты -->
    <section>
      <h2 class="text-3xl font-semibold text-slate-700 mb-4">Contact Us</h2>
      <p class="text-slate-600 leading-relaxed mb-4">
        Have any questions or want more information? Feel free to reach out to us:
      </p>
      <div class="flex flex-col space-y-4">
        <p class="font-semibold">Email: <a href="mailto:support@photographer-aggregator.com" class="text-blue-600">support@photographer-aggregator.com</a></p>
        <p class="font-semibold">Phone: <a href="tel:+1234567890" class="text-blue-600">+1 (234) 567-890</a></p>
        <p class="font-semibold">Social Media: <a href="https://www.instagram.com" class="text-blue-600" target="_blank">@photographeraggregator</a></p>
      </div>
    </section>
  </div>
</template>

<script setup>
// Можно добавить логику, если нужно получать данные через API.
</script>

<style scoped>
/* Общие стили */
h1, h2 {
  color: #2D3748;
}

h1 {
  font-size: 2.5rem;
}

h2 {
  font-size: 2rem;
}


.text-orange-600 {
  color: #e0ab4a;
}

.font-semibold {
  font-weight: 600;
}

/* Стили для контейнера */
.max-w-lg {
  max-width: 36rem;
}

.bg-gradient-to-r {
  background-image: linear-gradient(to right, #efbb7cb3, #fbdd96);
}

.p-6 {
  padding: 1.5rem;
}

.p-8 {
  padding: 2rem;
}

/* Стили для списка преимуществ */
.list-disc {
  list-style-type: disc;
}

.space-y-3 > * {
  margin-bottom: 0.75rem;
}

.bg-orange-600 {
  background-color: #efbb7cb3;
}

</style>
