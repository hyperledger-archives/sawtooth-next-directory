var gulp = require('gulp');
var fs = require('fs');
var replace = require('gulp-replace');
var count = require('gulp-count');

gulp.task('test', [], function () {
    return console.log('test');
});

gulp.task('add-license', [], function () {
    var header = fs.readFileSync('header.txt', 'utf-8');
    console.log(header);
    var htmlHeader = '<!--' + header + '-->' +
        '';
    var jsHeader = '/*' + header + '*/';

    var jsSrc = ['./src/**/*.ts',
        './src/**/*.js',
        './src/**/*.scss',
        './src/**/*.css'
    ];

    var htmlSrc = ['./src/**/*.html'];

    gulp.src(jsSrc)
        .pipe(count('## files found'))
        .pipe(replace(/(\/\*([\s\S]*?)\*\/)|(\/\/(.*)$)/m, ''))
        .pipe(replace(/([^]*)/, jsHeader + '$1'))
        .pipe(gulp.dest('./src'));

    gulp.src(htmlSrc)
        .pipe(count('## files found'))
        .pipe(replace(/<!--[\s\S]*?-->/, ''))
        .pipe(replace(/([^]*)/, htmlHeader + '$1'))
        .pipe(gulp.dest('./src'));

});