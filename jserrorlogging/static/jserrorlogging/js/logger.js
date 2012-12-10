(function(g){
  var loaded = false, errors = [], inputPrefix = 'form',
      endpoint = g.endpoint, userAgent = navigator.userAgent, meta = g.meta,
      timer, sendError, getInputName, generateForm, pushError, parseStack;
  /**
   * proceed and push error data
   *
   */
  pushError = function (error) {
    if(timer) { clearTimeout(timer); }
    errors.push({
      message: error[0],
      url: error[1],
      line: error[2],
      page: location.href,
      user_agent: userAgent,
      when: loaded ? 'after': 'before'
    });
    timer = setTimeout(sendError, 200);
  };

  /**
   * send error data to server
   *
   */
  sendError = function() {
    var iframe;
    try {
      iframe = generateForm();
      setTimeout(function(){
        iframe.parentNode.removeChild(iframe);
      }, 10000);
    } catch(m) {
      // pass
    }
  };

  getInputName = function(name, count) {
    return [inputPrefix, count, name].join('-');
  };

  generateInput = function(name, data) {
    val = (String() + data).replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/'/g, "&quot;");
    return "<input name='" + name + "' value='" + val + "' />";
  };

  /**
   * generate DOM elements
   *
   */
  generateForm = function() {
    var cnt = errors.length, errs = [],
        name, err, val, i, j, script, iframe, form, content;
    script = document.getElementsByTagName('script')[0];
    iframe = document.createElement('iframe');
    // for ssl
    iframe.src = ['javascript', ':', 'false;'].join('');
    iframe.style.display = 'none';
    script.parentNode.insertBefore(iframe, script);
    form = ['<form method="post" action="' + endpoint + '">'];
    for(i = 0; i < cnt; i++) {
      err = errors.shift();
      for(name in err) {
        if (err.hasOwnProperty(name)) {
          form.push(generateInput(getInputName(name, i), err[name]));
        }
      }
      j = 0;
      for(name in meta) {
        if(meta.hasOwnProperty(name)) {
          form.push(generateInput(inputPrefix + i + '-' + j + '-name', name));
          form.push(generateInput(inputPrefix + i + '-' + j + '-value', meta[name]));
          j++;
        }
      }
      if(j > 0) {
        form.push(generateInput(inputPrefix + i + '-INITIAL_FORMS', 0));
        form.push(generateInput(inputPrefix + i + '-TOTAL_FORMS', j));
      }
    }
    form.push(generateInput(inputPrefix + '-INITIAL_FORMS', 0));
    form.push(generateInput(inputPrefix + '-TOTAL_FORMS', i));
    form.push('</form>');
    form.push('<script>');
    form.push('window.onload=function(){setTimeout(function(){document.getElementsByTagName("form")[0].submit()}, 10);}');
    form.push('</script>');
    form = form.join('');
    content = iframe.contentWindow || iframe.contentDocument;
    doc = content.document || content;
    doc.open();
    doc.write(form);
    doc.close();
    return iframe;
  };

  if(g.errors.length > 0) {
    pushError(g.errors.shift());
  }
  loaded = true;
  g.errors = {push: pushError, meta: g.meta};
}(djjserr));
