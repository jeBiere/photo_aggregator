<template>
  <div class="bg-white p-6 rounded-lg shadow-md mt-8 border border-orange-200">
    <h2 class="text-2xl font-semibold text-slate-700 mb-4">Manage Your Working Hours</h2>
    <div class="grid grid-cols-7 gap-4">
      <div v-for="(day, index) in daysOfWeek" :key="index" class="flex flex-col items-center">
        <span class="font-semibold text-slate-600">{{ day }}</span>
        <Select v-model="schedule[index].start" :options="hourOptions" placeholder="Start Time" />
        <Select v-model="schedule[index].end" :options="hourOptions" placeholder="End Time" />
      </div>
    </div>
    <div class="flex justify-center mt-6">
      <Button label="Save Schedule" @click="saveSchedule" />
    </div>
    <div class="mt-8">
      <h3 class="text-xl font-semibold text-slate-600 mb-4">Add Time Off / Exceptions</h3>
      <div class="flex flex-col gap-4">
        <div class="flex gap-2">
          <label class="font-semibold text-slate-600">Date:</label>
          <input type="date" v-model="exceptionDate" class="border rounded-xl p-2 custom-input" />
        </div>
        <div class="flex gap-2 items-center">
          <label class="font-semibold text-slate-600">Time Off (Start):</label>
          <Select v-model="exceptionStart" :options="hourOptions" placeholder="Start Time" />
          <label class="font-semibold text-slate-600">End Time:</label>
          <Select v-model="exceptionEnd" :options="hourOptions" placeholder="End Time" />
        </div>
        <div class="flex justify-center">
          <Button label="Add Time Off" @click="addException" class="w-auto" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Button from '@/components/Button.vue'
import Select from '@/components/Select.vue'
import { useAuthStore } from '@/stores/authStore'

const authStore = useAuthStore()

const daysOfWeek = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
const availableHours = Array.from({ length: 24 }, (_, i) => i)
const hourOptions = availableHours.map((hour) => ({
  label: `${hour}:00`,
  value: hour
}))

const schedule = ref(Array.from({ length: 7 }, () => ({ start: '', end: '' })))
const exceptionDate = ref('')
const exceptionStart = ref('')
const exceptionEnd = ref('')

const saveSchedule = () => {
  console.log('Schedule saved:', schedule.value)
}

const addException = () => {
  console.log('Exception added:', {
    exceptionDate: exceptionDate.value,
    exceptionStart: exceptionStart.value,
    exceptionEnd: exceptionEnd.value
  })
}

onMounted(async () => {
  try {
    const headers = { Authorization: `Bearer ${authStore.token}` }
    const res = await axios.get('http://localhost:8000/schedules/working-hours/me', { headers })
    const workingHours = res.data

    workingHours.forEach(({ day_of_week, start_time, end_time }) => {
      const startHour = parseInt(start_time.split(':')[0])
      const endHour = parseInt(end_time.split(':')[0])
      schedule.value[day_of_week] = {
        start: startHour,
        end: endHour
      }
    })
  } catch (err) {
    console.error('Ошибка при загрузке рабочих часов:', err)
  }
})
</script>

<style scoped>
.custom-input {
  @apply bg-white border rounded-xl p-2 text-slate-600 font-medium shadow-md focus:outline-none focus:ring-2 focus:ring-orange-300;
}

button:focus,
.custom-input:focus {
  @apply ring-2 ring-orange-300;
}

button {
  @apply bg-orange-100 hover:bg-orange-200 text-slate-600 font-bold py-2 px-4 rounded-3xl mt-8 transition ease-in-out duration-300 uppercase;
}

button.w-auto {
  width: auto;
}
</style>
