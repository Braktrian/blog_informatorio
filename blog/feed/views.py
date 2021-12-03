from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from feed.models import *




#---------------------------------------------------------------------------------------------------
#                                    VISTAS PARA EL PRIMER SPRINT
#---------------------------------------------------------------------------------------------------


def feed(request):
    posteos = post.objects.all().order_by('creado_en').reverse() 
    categorias = categoria.objects.all()
    return render(request,"feed.html",{'posteos':posteos,'categorias':categorias})

def leer_posteo(request,id):
    un_posteo=post.objects.get(id=id)
    comentarios_del_posteo = comentario.objects.filter(post_id=id)
    return render(request,"leer_post.html",{'un_posteo':un_posteo, 'comentarios_del_posteo':comentarios_del_posteo})

#agragar bien el tipo_17_ods
@login_required
def agregar_post(request):
    titulo = request.POST['txttitulo']
    contenido = request.POST['txtcontenido']
    imagen = request.FILES.get('txtimagen','post_default.jpg')
    categoria_match = request.POST.get('txtcategoria')
    pre_contenido = str(contenido)[0:60] + "[...]"
    usuario_match = User.objects.get(id = request.user.id)
    if titulo != "" and contenido != "":
        post_creado = post.objects.create(titulo=titulo,contenido=contenido,posteador=usuario_match,pre_contenido=pre_contenido, categoria_id=categoria_match,imagen=imagen)
        post_creado.save()
        messages.success(request, 'Post creado correctamente')
    else:
        messages.warning(request, 'Hay campos vacios')
    return redirect('perfil_usuario')


def registrarse(request):
    tipo_usuario_match = tipo_usuario.objects.all()
    return render(request,"registrarse.html",{'tipo_usuario_match':tipo_usuario_match})


def crear_usuario(request):
    nombre = request.POST['txtnombre']
    email = request.POST['txtemail']
    password = request.POST['txtpassword']
    password2 = request.POST['txtpassword2']
    rol = request.POST.get('txttrol')
    foto = request.FILES.get('txtimagen','foto_default.jpg')
    if nombre != "" and email != "" and password != "" and password2 != "" and rol != "":
        usename_exists = User.objects.filter(username=nombre).exists()
        if usename_exists:
            messages.warning(request, 'El usuario ya existe')
        else:
            if password == password2:
                usuario_creado = User.objects.create_user(username=nombre,email=email,password=password)
                usuario_creado.save()
                usuario_rol = usuario.objects.create(usuario_fk_id=usuario_creado.id ,tipo_usuario_id=rol,foto=foto)
                usuario_rol.save()
                messages.success(request, 'Usuario creado correctamente')
                return redirect('acceder')
            else:
                messages.warning(request, 'Las contraseñas no coinciden')
    else:
        messages.warning(request, 'Hay campos vacios')
    return redirect('registrarse')


def acceder(request):
    return render(request,"registration/login.html")



#--------------arreglar el iniciar sesion en la parte-------------
def iniciar_sesion(request):
    nombre = request.POST['txtusuario']
    contrasenia = request.POST['txtpassword']
    if nombre != "" and contrasenia !="":
        usuario_existe = User.objects.filter(username=nombre).exists()
        if usuario_existe:
            print("usuario existe y es",usuario_existe)
            user = authenticate(request, username=nombre, password=contrasenia)
            print("autenticador",user, nombre,contrasenia)
            if user is not None:
                login(request,user)
                messages.success(request, f'Bienvenido {nombre}')
                return redirect('feed')
            else:
                messages.warning(request, 'Usuario y/o contraseña incorrectos')
        else:
            messages.warning(request, 'Usuario no existe')
    else:
        messages.warning(request, 'Hay campos vacios')
    return redirect('acceder')

#---------------------------------------------------------------------------------------------------
#                                     VISTAS PARA EL SEGUNDO SPRINT
#---------------------------------------------------------------------------------------------------

#configurar a que post va el comentario y por quien es creado
@login_required
def crear_comentario(request):
    contenido = request.POST['txtcontenido']
    usuario_match = usuario.objects.get(id=request.user.id)
    if comentario != "" and contenido != "":
        comentario_creado = comentario.objects.create(contenido=contenido, comentador=usuario_match, post_id=1)
        comentario_creado.save()
        messages.success(request, 'Comentario creado correctamente')
    else:
        messages.warning(request, 'Hay campos vacios')

    return redirect('leer_posteo',id)


@login_required
def perfil_usuario(request):
    print('request',request.user.id)
    posteos = post.objects.filter(posteador_id=request.user.id)
    comentarios = comentario.objects.filter(comentador_id=request.user.id)
    categorias = categoria.objects.all()
    return render(request,"perfil_usuario.html",{'posteos':posteos, 'comentarios':comentarios, 'categorias':categorias})


def buscar_por_catetoria(request,id):
    posteos = post.objects.filter(categoria_id=id).order_by('creado_en').reverse()
    categorias = categoria.objects.all()
    return render(request,"feed.html",{'posteos':posteos,'categorias':categorias})
    

def busqueda_por_fecha(request,fecha):
    posteos = post.objects.filter(fecha=fecha)
    return render(request,"feed.html",{'posteos':posteos})

def busqueda_por_comentario(request,comentatario_buscado):
    posteos = post.objects.filter(comentario_contains=comentatario_buscado)
    return render(request,"feed.html",{'posteos':posteos})



#---------------------------------------------------------------------------------------------------
#                                     VISTAS PARA EL TRECER SPRINT
#---------------------------------------------------------------------------------------------------


@login_required
def eliminar_post(request,id):
    post_eliminado = post.objects.get(id=id)
    post_eliminado.delete()
    messages.success(request, 'Post eliminado correctamente')
    return redirect('perfil_usuario')

@login_required
def editar_post(request,id):
    post_editar = post.objects.get(id=id)
    return render(request,"editar_post.html",{'post_editar':post_editar})


@login_required
def editar_post_guardar(request,id):
    titulo = request.POST['txttitulo']
    contenido = request.POST['txtcontenido']
    if titulo != "" and contenido != "":
        post_editar = post.objects.get(id=id)
        post_editar.titulo = titulo
        post_editar.contenido = contenido
        post_editar.save()
        messages.success(request, 'Post editado correctamente')
    else:
        messages.warning(request, 'Hay campos vacios')
    return redirect('perfil_usuario')

@login_required
def eliminar_comentario(request,id):
    comentario_eliminado = comentario.objects.get(id=id)
    comentario_eliminado.delete()
    messages.success(request, 'Comentario eliminado correctamente')
    return redirect('perfil_usuario')



#---------------------------------------------------------------------------------------------------
#                                     VISTAS PARA EL CUARTO SPRINT
#---------------------------------------------------------------------------------------------------

def dar_me_gusta(request,id):
    post_me_gusta = post.objects.get(id=id)
    post_me_gusta.me_gusta += 1
    post_me_gusta.save()
    return redirect('leer_posteo',id)

def dar_no_me_gusta(request,id):
    post_no_me_gusta = post.objects.get(id=id)
    post_no_me_gusta.no_me_gusta += 1
    post_no_me_gusta.save()
    return redirect('leer_posteo',id)


def editar_perfil(request,id):
    usuario_editar = usuario.objects.get(id=id)
    return render(request,"editar_perfil.html")

def editar_perfil_guardar(request,id):
    nombre = request.POST['txtnombre']
    email = request.POST['txtemail']
    foto = request.POST['txtfoto']
    if nombre != "" and email != "":
        usuario_editar = usuario.objects.get(id=id)
        usuario_editar.nombre = nombre
        usuario_editar.email = email
        usuario_editar.foto = foto
        usuario_editar.save()
        messages.success(request, 'Perfil editado correctamente')
    else:
        messages.warning(request, 'Hay campos vacios')
    return redirect('perfil_usuario')