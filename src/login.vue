<template>
	<div class="center">
		<h1>登录/注册</h1>
		<div class="logon">
			<div :class="overlaylong">
				<div class="overlaylong-Signin" v-if="disfiex == 0">
					<h2 class="overlaylongH2">登录</h2>
					<el-form :model="loginForm" :rules="loginRules" ref="loginForm">
						<el-form-item prop="email">
							<input type="text" placeholder="email" v-model="loginForm.email">
						</el-form-item>
						<el-form-item prop="password">
							<input type="password" placeholder="password" v-model="loginForm.password">
						</el-form-item>
					</el-form>
					<h3>忘记密码</h3>
					<el-button class="inupbutton" @click="login()">登录</el-button>
				</div>
				<div class="overlaylong-Signup" v-if="disfiex == 1">
					<h2 class="overlaylongH2">注册</h2>
					<el-form :model="registerForm" :rules="registerRules" ref="registerForm">
						<el-form-item prop="email">
							<input type="text" placeholder="邮箱" v-model="registerForm.email">
						</el-form-item>
						<el-form-item>
							<el-button @click="getVerifyCode(); buttonText = '已发送'">{{ buttonText }}</el-button>
						</el-form-item>
						<el-form-item prop="captcha">
							<input type="text" placeholder="验证码" v-model="registerForm.captcha">
						</el-form-item>
						<el-form-item prop="password">
							<input type="password" placeholder="密码" v-model="registerForm.password">
						</el-form-item>
						<el-form-item prop="pass2">
							<input type="password" placeholder="确认密码" v-model="registerForm.pass2">
						</el-form-item>
					</el-form>
					<el-button class="inupbutton" @click="register()">注册</el-button>
				</div>

			</div>
			<div :class="overlaytitle">
				<div class="overlaytitle-Signin" v-if="disfiex == 0">
					<h2 class="overlaytitleH2">Hello,Friend!</h2>
					<p class="overlaytitleP">
						如果没有账户，点击注册
					</p>
					<div class="buttongohs" @click="disfiex = 1">注册</div>
				</div>
				<div class="overlaytitle-Signup" v-if="disfiex == 1">
					<h2 class="overlaytitleH2">Welcome Back!</h2>
					<p class="overlaytitleP">
						如果已经有账户，去登陆
					</p>
					<div class="buttongohs" @click="disfiex = 0">登录</div>
				</div>
			</div>
		</div>

	</div>
</template>

<script>
import { login, sendVerifyCode, register } from '@/service/authService.js'
export default {
	name: "login",
	data() {

		var validPass = (rule, value, callback) => {
			if (value === '') {
				callback(new Error('请再次输入密码'));
			} else if (value !== this.registerForm.password) {
				callback(new Error('两次输入密码不一致!'));
			} else {
				callback();
			}
		}
		return {
			overlaylong: 'overlaylong',
			overlaytitle: 'overlaytitle',
			disfiex: 1,
			buttonText: '发送验证码',
			loginForm: {
				email: '',
				password: ''
			},
			registerForm: {
				email: '',
				password: '',
				pass2: '',
				captcha: '',

			},
			loginRules: {
				email: [
					{ required: true, message: '请输入邮箱', trigger: 'blur' }
				],
				password: [
					{ required: true, message: '请输入密码', trigger: 'blur' }
				]
			},
			registerRules: {
				email: [
					{ required: true, message: '请输入邮箱', trigger: 'blur' }
				],
				password: [
					{ required: true, message: '请输入密码', trigger: 'blur' }
				],
				captcha: [
					{ required: true, message: '请输入验证', trigger: 'blur' },
					{ min: 6, max: 6, message: '请输入6位验证码', trigger: 'blur' }
				],
				pass2: [
					{ validator: validPass, trigger: 'blur' }
				]
			},

		}
	},

	methods: {
		login() {
			this.$refs["loginForm"].validate(valid => {
				if (valid) {
					console.log('valid', valid);
					login(this.loginForm).then(res => {
						console.log(res)
					}).cache(e => {
						// console.log(e)
					})
				} else {
					return false;
				}
			})
		},
		register() {
			this.$refs["registerForm"].validate(valid => {
				if (valid) {
					console.log('valid', valid);

					register(this.registerForm).then(res => {
						ElMessage({
							message: '注册成功',
							type: 'success'
						})
					})
				} else {
					return false;
				}
			})

		},
		getVerifyCode() {
			sendVerifyCode(this.registerForm.email).then(res => {
				ElMessage({
					message: '发送成功',
					type: 'success'
				})
			})
		}
	}
}
</script>

<style scoped>
.center {
	width: 1920px;
	height: 1080px;
	background-image: url('./assets/bg.jpeg');
	background-size: 100% 100%;
	background-repeat: no-repeat;
	display: flex;
	align-items: center;
	justify-content: center;
	flex-direction: column;
}

h1 {
	font-size: 30px;
	color: black;
}

.logon {
	background-color: #fff;
	border-radius: 10px;
	box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22);
	/* position: relative;
		overflow: hidden; */
	width: 768px;
	max-width: 100%;
	min-height: 480px;
	margin-top: 20px;
	display: flex;
	background: -webkit-linear-gradient(right, #4284db, #29eac4);
}

.overlaylong {
	border-radius: 10px 0 0 10px;
	width: 50%;
	height: 100%;
	background-color: #fff;
	display: flex;
	align-items: center;
	justify-content: center;
}

.overlaylongleft {
	border-radius: 0px 10px 10px 0px;
	width: 50%;
	height: 100%;
	background-color: #fff;
	transform: translateX(100%);
	transition: transform 0.6s ease-in-out;
	display: flex;
	align-items: center;
	justify-content: center;
}

.overlaylongright {
	border-radius: 10px 0 0 10px;
	width: 50%;
	height: 100%;
	background-color: #fff;
	transform: translateX(0%);
	transition: transform 0.6s ease-in-out;
	display: flex;
	align-items: center;
	justify-content: center;
}

.overlaytitle {
	border-radius: 0px 10px 10px 0px;
	width: 50%;
	height: 100%;
	background-color: rgba(0, 0, 0, 0);
	display: flex;
	align-items: center;
	justify-content: center;
}


.overlaytitleH2 {
	font-size: 30px;
	color: #fff;
	margin-top: 20px;
}

.overlaytitleP {
	font-size: 15px;
	color: #fff;
	margin-top: 20px;
}

.overlaytitleleft {
	border-radius: 0px 10px 10px 0px;
	width: 50%;
	height: 100%;
	background-color: rgba(0, 0, 0, 0);
	display: flex;
	align-items: center;
	justify-content: center;
	transform: translateX(0%);
	transition: transform 0.6s ease-in-out;
}

.overlaytitleright {
	border-radius: 0px 10px 10px 0px;
	width: 50%;
	height: 100%;
	background-color: rgba(0, 0, 0, 0);
	display: flex;
	align-items: center;
	justify-content: center;
	transform: translateX(-100%);
	transition: transform 0.6s ease-in-out;
}

.overlaytitle-Signin {
	display: flex;
	align-items: center;
	justify-content: center;
	flex-direction: column;
}

.overlaytitle-Signup {
	display: flex;
	align-items: center;
	justify-content: center;
	flex-direction: column;
}

.buttongohs {
	width: 180px;
	height: 40px;
	border-radius: 50px;
	border: 1px solid #fff;
	color: #fff;
	font-size: 15px;
	text-align: center;
	line-height: 40px;
	margin-top: 40px;
	cursor: pointer;
}

.overlaylongH2 {
	font-size: 25px;
	color: black;
	/* width: 250px; */
}

.overlaylong-Signin {
	display: flex;
	align-items: center;
	justify-content: center;
	flex-direction: column;
}

.overlaylong-Signup {
	display: flex;
	align-items: center;
	justify-content: center;
	flex-direction: column;
}

input {
	background-color: #eee;
	border: none;
	padding: 12px 15px;
	margin: 10px 0;
	width: 240px;
}

h3 {
	font-size: 10px;
	margin-top: 10px;
	cursor: pointer;
}

.inupbutton {
	background-color: #29eac4;
	border: none;
	width: 180px;
	height: 40px;
	border-radius: 50px;
	font-size: 15px;
	color: #fff;
	text-align: center;
	line-height: 40px;
	margin-top: 30px;
}
</style>
