module.exports = function(grunt) {
  grunt.initConfig({
    min: {
      dist: {
        src: ['js/logger.js'],
        dest: 'js/logger.min.js'
      }
    }
  });
  grunt.registerTask('default', 'min');
};
