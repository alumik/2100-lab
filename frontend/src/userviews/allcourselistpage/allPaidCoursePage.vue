<template>
  <AllCourseList
    id="all-paid"
    :page_title="page_title"
    :course_list="course_list"/>
</template>

<script>
import AllCourseList from '../components/allCourseList'

export default {
  name: 'AllFreeCoursePage',
  components: {
    AllCourseList
  },
  data () {
    return {
      page_title: '付费课程',
      course_list: [
        {
          id: 4,
          name: '不爱我就拉倒',
          introduction: '环滁皆山也。其西南诸峰，林壑尤美，' +
            '望之蔚然而深秀者，琅琊也。',
          src: require('../components/image/7.jpg')
        }
      ]
    }
  }
}
</script>
