import { mount } from '@vue/test-utils'
import Envar from '../../src/views/EnvVar.vue'

test('check environment variables', async() => {
  expect(Envar).toBeTruthy()

  const wrapper = mount(Envar)

  expect(wrapper.text()).toContain('NODE_ENV (defined)')
  expect(wrapper.text()).toContain('VUE_APP_CLOUD_BASE_URL (defined)')
  expect(wrapper.text()).toContain('VUE_APP_AUTH0_AUDIENCE (defined)')
  expect(wrapper.text()).toContain('VUE_APP_AUTH0_ISSUER (defined)')
  expect(wrapper.text()).toContain('VUE_APP_AUTH0_FRONT_ID (defined)')
  expect(wrapper.text()).toContain('BASE_URL (defined)')
})