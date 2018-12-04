import sox

def getTransformer(request):
    tfm = sox.Transformer()
    if request.form.getlist('reverb'):
        rev = float(request.form.get('reverb_reverberance',50))
        hfd = float(request.form.get('reverb_high_freq_damping',50))
        rsc = float(request.form.get('reverb_room_scale',100))
        tfm.reverb(reverberance=rev,high_freq_damping=hfd,room_scale=rsc)
    if request.form.getlist('echo'):   
        gin = float(request.form.get('echo_gain_in',0.8))
        gou = float(request.form.get('echo_gain_out',0.9))
        #Todo need to parse list of float
        # nec = int(request.form.get('echo_n_echos',1))
        # dea = request.form.get('echo_delays',[60])
        # dec = request.form.get('echo_decays',[0.4])
        tfm.echo(gain_in=gin,gain_out=gou)
    return tfm