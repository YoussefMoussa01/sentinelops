import { fork } from 'redux-saga/effects'
import authSaga from '@/features/auth/sagas/authSagas'

export default function* rootSaga() {
  yield fork(authSaga)
  // Additional sagas will be added in future phases
}
