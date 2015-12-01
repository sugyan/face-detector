/* eslint-env node */
var gulp = require('gulp');
var babel = require('gulp-babel');

gulp.task('build', function() {
    return gulp.src('src/js/*.js')
        .pipe(babel({ presets: ['es2015'] }))
        .pipe(gulp.dest('static/js'));
});

gulp.task('default', ['build']);
