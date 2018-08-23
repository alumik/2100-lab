<template>
  <Basic>
    <div class="container">
      <img src="../../assets/logo.png">
      <h2>2100实验室</h2>
      <br>
      <b-input-group prepend="手机号">
        <b-form-input
          v-model="phone"
          :state="phoneState"
          type="text"/>
        <b-form-invalid-feedback id="inputLiveFeedback">
          手机号码不正确！
        </b-form-invalid-feedback>
      </b-input-group>
      <br>
      <b-input-group prepend="验证码">
        <b-form-input
          v-model="code"
          :state="codeState"
          type="text"
          aria-describedby="inputLiveFeedback"/>
        <b-input-group-append>
          <b-btn
            id="send"
            :disabled="disabled"
            variant="outline-success"
            @click="send">{{ status }}{{ second }}</b-btn>
        </b-input-group-append>
        <b-form-invalid-feedback id="inputLiveFeedback">
          验证码不正确！
        </b-form-invalid-feedback>
      </b-input-group>
      <br>
      <b-button
        id="btn"
        type="submit"
        variant="success"
        @click="login">登录
      </b-button>
      <b-modal
        v-model="modalShow"
        :ok-disabled="okDisabled"
        size="lg"
        title="用户协议"
        centered
        ok-title="我同意"
        cancel-title="返回"
        @ok="handleOk">
        {{ content }}
        <br>
        <b-form-checkbox
          id="checkbox"
          v-model="accept"
          value="accepted">
          我同意该协议
        </b-form-checkbox>
      </b-modal>
    </div>
  </Basic>
</template>

<script>
import Basic from '../components/basic'
import axios from 'axios'
import qs from 'qs'
export default {
  name: 'Login',
  components: {
    Basic
  },
  data () {
    return {
      phone: '',
      code: '',
      correct_code: '',
      status: '获取验证码',
      codeState: true,
      phoneState: true,
      seconds: 61,
      disabled: false,
      okDisabled: true,
      modalShow: false,
      accept: '',
      content:
        '使用协议\n' +
        '计蒜客主要依靠网络技术，通过计蒜客平台向您提供在线学习与移动学习服务。请您在注册账号和使用计蒜客前仔细阅读本协议。如您不同意本协议任何条款，请勿申请账号或使用本平台。\n' +
        '\n' +
        '一、注册协议条款的确认和接受\n' +
        '本协议双方为北京矩道优达网络科技有限公司旗下网站计蒜客（以下亦称“本网站”）和计蒜客注册学生（以下亦称“学生”）。本协议阐述之条款和条件适用于本网站（www.jisuanke.com）的全部学习服务，包括但不限于各种课程学习内容、源代码、资料及相应服务。\n' +
        '本网站按照本协议的规定以及不定时发布的操作规则提供基于互联网和移动互联网的相关服务（以下称“服务”）。为获取服务，申请人应当认真阅读、充分理解本协议中各条款，包括免除或者限制本网站责任的免责条款及对学生的权利限制条款。认真阅读并选择接受或不接受本协议（未成年人应在法定监护人陪同下阅读）。同意接受本协议的全部条款的，申请人应当按照页面上的提示完成全部的申请程序，否则视为不接受本协议全部条款，申请人应当终止并退出申请。\n' +
        '学生在使用本网站的服务时，应承诺接受并遵守各项相关规则的规定。本网站有权根据实际运营需要而不定时修改本协议或补充本协议，如本协议有任何变更，将通过网站消息或其他方式通知学生。如学生不同意相关变更，则应立即终止账号使用，否则即视为学生同意并完全接受修订后的协议版本。经修订的协议一经公布于本网站的网站链接及页面，立即自动生效，亦成为本协议的一部分。除书面另行声明外，任何扩大的服务范围及新增提供的内容均受本协议约束。\n' +
        '二、学生的权利和义务\n' +
        '学生在注册时应按照申请提示提供昵称、密码及真实的联系邮箱、手机号码、姓名等所要求的个人资料，并定期更新资料，符合及时、详尽、准确的要求，学生输入的所有个人信息将被视作学生的准确身份信息。\n' +
        '如果学生提供的资料包含有不正确或不良的信息，本网站保留终止学生使用服务资格的权利。\n' +
        '在支付课程费用并经本网站确认后，学生有权通过其在本网站申请的账号享受相应的服务。具体服务内容的时间、进度及期限以本网站的具体课程及产品说明、公告及其内容为准。\n' +
        '本网站的学生账号只为学生本人所专有并仅限由其本人自己使用。一个学生账号同一时间只能在一台终端设备上登录并使用，且一个学生账号至多只能在学生本人所有的五台不同的终端设备上登录并使用。\n' +
        '未经本网站许可，不得以任何形式向第三方转让、授权、出售本网站课程、服务或授权第三方使用学生账号，不得以任何形式通过本网站内容进行盈利性活动，不得在商业环境下展映、传播本网站教学内容。\n' +
        '学生仅对其在本网站上享有的服务及内容有使用权，并不对该内容拥有相关知识产权。未经本网站或其他有权第三方的许可，学生不得对本网站的任何内容进行翻录、复制、发行、破解、信息网络传播或其他违反知识产权相关法律、法规的行为，否则所导致的一切民事、行政或刑事责任，由学生自行承担。\n' +
        '对于学生在本网站中所下载的任何标有本网站的资料，学生只得根据具体的使用协议进行使用，并不拥有该产品及产品中任何内容的一切知识产权。除非经相应的产品使用协议许可，学生不得自行或授权他人对软件或其中的任何一部分进行复制、反编译、倒序制造、反汇编、试图推导源代码、破译、修改或创作衍生作品，因此而造成本网站或任何第三方的损失，由学生承担全部责任。本网站对上述侵权或违约行为保留追索的权利。\n' +
        '对于学生在本网站提交的问题及上传的文件或文档，学生同意本网站对此内容享有复制、发行及独家的出版权。\n' +
        '学生应对其账号的全部使用行为承担责任，应严格遵守本协议、相关法律法规、账号及课程使用规定。未经本网站许可，禁止学生向任何第三方提供本网站中的任何内容或资料。\n' +
        '学生应自行配备上网的所需设备，包括个人电脑、调制解调器或其他必备上网装置；学生应自行负担因使用这种接入方式而产生的上网电话费、上网信息费等费用。\n' +
        '本网站的所有服务均附期限，学生应在截止日期前享受其购买的服务。因服务到期终止所导致的任何后果，本网站不承担任何责任。\n' +
        '学生在本网站充值（包括但不限于通过网上支付、邮局汇款、银行电汇、上门购买并现金支付等各种购买方式），一经购买都不允许任何形式的退换和退费。\n' +
        '学生在账号使用过程中不得制作、复制、发布、传播含有下列内容的信息：\n' +
        '反对宪法所确定的基本原则的；\n' +
        '危害国家安全，泄露国家秘密，颠覆国家政权，破坏国家统一的；\n' +
        '损害国家荣誉和利益的；\n' +
        '煽动民族仇恨、民族歧视，破坏民族团结的；\n' +
        '破坏国家宗教政策，宣扬邪教和封建迷信的；\n' +
        '散布谣言，扰乱社会秩序，破坏社会稳定的；\n' +
        '散布淫秽、色情、赌博、暴力、凶杀、恐怖或者教唆犯罪的；\n' +
        '侮辱或者诽谤他人，侵害他人合法权益的；\n' +
        '干扰或者侵犯计蒜客的正常运行和秩序，影响其他学生正常使用的；\n' +
        '含有法律、行政法规禁止的其他信息内容的。\n' +
        '学生将自行承担学生账号使用过程中可能发生的风险和损失。\n' +
        '学生对本协议或将来的修改版本有任何异议的，或对产品服务存有异议或不满的，可以通过邮件（contact@jisuanke.com）向本网站进行反映沟通，不得通过煽动、诋毁及通过散布其他不良信息的方式进行。\n' +
        '三、学生的违约责任\n' +
        '学生如违反本协议第二条第四款、第五款、第六款、第七款的规定，本网站将视其情况停止学生所享有的服务 2 天至 60 天不等，情况及影响恶劣者，本网站有权立即终止向其提供服务，并删除其账号信息。\n' +
        '学生如违反本协议第二条第十三款规定，本网站将立即终止向其提供的服务，同时保存有关记录，并向国家有关机关报告。\n' +
        '学生如违反本协议约定，应赔偿所造成的本网站全部经济损失，包括但不限于律师费、公证费、赔偿金及行政处罚金等，并承担其他法律责任。\n' +
        '学生因违约而导致对任何第三方的侵权或任何索赔，均应由学生独自并完全承担，并且学生应赔偿本网站为此所遭受的全部经济损失。如该赔偿已由本网站清付，学生应立即全数（含利息）偿还，并且学生应赔偿本网站为此所遭受的商誉的损失。\n' +
        '四、本网站的权利和义务\n' +
        '本网站有义务通过现有技术维护本网站的正常运行，并努力提升和改进服务使学生的学习活动得以顺利进行；由于不可抗力所导致服务的中止或终止，本网站不对学生因此受到的任何损失承担责任。\n' +
        '学生在注册及使用本网站过程中遇到的相关问题，本网站将力争及时作出反馈。\n' +
        '如因系统维护或升级而需暂停服务时，本网站应提前告知学生。\n' +
        '本网站不保证其服务一定能够满足学生的全部要求，也不担保其服务不会因各种客观原因中断。\n' +
        '五、免责条款\n' +
        '当学生所享有的服务中显示其他第三方网站或内容时，由于本网站无法控制及审核该网站或内容，因此并不对该网站或内容真实性、有效性、合法性等效力承担责任。对于学生任何因使用或信赖该网站或内容所导致的任何直接或间接损失，本网站不负任何责任。\n' +
        '由于学生将个人学生账号信息告知他人或与他人共享学生账号而导致任何风险或损失，本网站不负任何责任。\n' +
        '任何由于黑客攻击、计算机病毒侵入或发作、政府管制、硬件故障、不可抗力等非本网站故意或严重过失而造成的学生个人资料泄露、丢失、被盗用、被篡改或服务暂定或终止，对学生所造成的风险或损失，本网站不负任何责任。\n' +
        '若因线路及非本网站控制范围内的或其他不可抗力而导致暂停服务暂定或终止，所造成的一切风险与损失，本网站不负任何责任。\n' +
        '本网站有权根据学生的实际需求进行服务调整的权利，并有权根据实际情况调整本网站内容的售价，由此造成的一切不便与损失，本网站不负任何责任。\n' +
        '在提前至少三个月告知学生的情况下，本网站有权利删减本网站的课程。\n' +
        '六、隐私条款\n' +
        '本网站将严格履行学生个人隐私保密义务，承诺不公开、编辑或透露学生个人信息，但以下情况除外：\n' +
        '\n' +
        '经学生授权透露部分或全部个人信息；\n' +
        '应政府部门、法律及法规要求提供、披露相关学生个人资料；\n' +
        '在特定情况下，为竭力维护学生个人、其他社会个体和公共安全需要。\n' +
        '七、法律\n' +
        '本协议根据现行中华人民共和国法律法规制定并解释。如发生协议条款与中华人民共和国法律法规相抵触时，则抵触的内容将按法律规定重新解释，但不影响其他条款的效力。\n' +
        '\n' +
        '八、解释权\n' +
        '上述条款的解释权在法律允许的范围内归本网站所有。',
      course_id: -1
    }
  },
  computed: {
    second () {
      if (this.seconds < 61) {
        return this.seconds + 's'
      }
      return ''
    }
  },
  watch: {
    accept: function (o) {
      if (o === 'accepted') {
        this.okDisabled = false
      }
    },
    phone: function (n) {
      if (n.length > 11) {
        this.phoneState = false
      } else {
        this.phoneState = true
      }
    },
    code: function (n) {
      if (n.length > 6) {
        this.codeState = false
      } else {
        this.codeState = true
      }
    }
  },
  mounted () {
    if (this.$route.params.source === 'coursedetail') {
      this.course_id = this.$route.params.course_id
    }
  },
  methods: {
    send () {
      let that = this
      axios
        .post(
          'http://localhost:8000/api/v1/customers/forestage/auth/get-verification-code/',
          qs.stringify({
            phone_number: this.phone
          }),
          { withCredentials: true }
        )
        .then(response => {
          alert(response.data.verification_code)
          that.$store.commit('new_customer', response.data.is_customer)
          that.status = '再次发送 '
          that.seconds = that.seconds - 1
          that.disabled = true
          let t = setInterval(function () {
            that.seconds = that.seconds - 1
            if (that.seconds === -1) {
              that.disabled = false
              that.seconds = 61
              clearInterval(t)
            }
          }, 1000)
        })
        .catch(error => {
          if (error) {
            that.phoneState = false
          }
        })
    },
    handleOk (evt) {
      if (this.accept === 'accepted') {
        this.$router.push({ path: '/personal' })
      }
      evt.preventDefault()
    },
    login () {
      let that = this
      axios
        .post(
          'http://localhost:8000/api/v1/customers/forestage/auth/authenticate-customer/',
          qs.stringify({
            phone_number: this.phone.toString(),
            verification_code: this.code.toString()
          }),
          { withCredentials: true }
        )
        .then(response => {
          if (response.data.is_new_customer) {
            this.modalShow = !this.modalShow
            this.$store.commit('new_customer')
          } else {
            this.$store.commit('status')
            this.$store.commit('user', response.data)
            this.$store.commit('phone', this.phone)
            if (this.course_id !== -1) {
              this.$router.push({
                path: '/coursedetail',
                query: { course_id: this.course_id }
              })
            }
            this.$router.push({ path: '/personal' })
          }
        })
        .catch(error => {
          if (error.response.data.message === 'Different phone number.') {
            that.phoneState = false
          } else if (
            error.response.data.message === 'Wrong verification code.'
          ) {
            this.codeState = false
          } else {
            alert('请刷新重试')
          }
        })
    }
  }
}
</script>

<style scoped>
.container {
  display: block;
  width: 350px;
  margin: 100px auto;
  text-align: center;
  border: 1px solid #ccc;
  border-radius: 10px;
  box-shadow: 5px 6px 5px rgba(0, 0, 0, 0.1);
}

img {
  width: 80%;
  height: 80%;
}

#btn {
  margin-bottom: 10px;
}
</style>
