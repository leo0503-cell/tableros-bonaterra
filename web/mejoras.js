(() => {
  'use strict';
  const $ = s => document.querySelector(s);
  const barra = $('#barra'), nav = barra.querySelector('nav');
  nav.id='menu-principal';
  const menu=document.createElement('button');menu.type='button';menu.className='menu-toggle';menu.textContent='Menú';menu.setAttribute('aria-controls',nav.id);menu.setAttribute('aria-expanded','false');barra.append(menu);
  function closeMenu(){barra.classList.remove('menu-abierto');menu.setAttribute('aria-expanded','false')}
  menu.onclick=()=>{const open=barra.classList.toggle('menu-abierto');menu.setAttribute('aria-expanded',String(open))};
  nav.addEventListener('click',closeMenu);document.addEventListener('keydown',e=>{if(e.key==='Escape')closeMenu()});
  $('.intro').insertAdjacentHTML('beforeend','<div class="hero-acciones"><a href="#materiales">Explorar materiales ↗</a><a href="#cotiza">Cotizar mi proyecto</a></div>');
  $('.mundo').insertAdjacentHTML('beforeend','<a class="materiales-vertical" href="#materiales" aria-label="Ver materiales: madera y polín, melamina y enchapados, MDF, triplay, PVC mármol, WPC lambrín, deck y más"><svg viewBox="190 0 350 2170" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><defs><filter id="sin-fondo-materiales" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  8 8 -16 0 -0.12"/></filter></defs><image href="img/materiales-vertical.png" width="725" height="2170" filter="url(#sin-fondo-materiales)"/></svg></a>');
  const iconosServicio={'Corte a medida':'corte','Envío a domicilio':'envio','Asesoría personalizada':'asesoria','Enchapado':'enchapado'};
  const materialesRail=$('.materiales-vertical');
  const tramos=[0,300,585,830,1070,1365,1640,1885,2170];
  const nombres=['Madera y polín','Melamina y enchapados','MDF','Triplay','PVC mármol','WPC lambrín','Deck','Y más'];
  const plantilla=materialesRail.querySelector('svg');
  materialesRail.replaceChildren(...nombres.map((nombre,i)=>{const icono=plantilla.cloneNode(true);icono.setAttribute('viewBox',`180 ${tramos[i]} 365 ${tramos[i+1]-tramos[i]}`);const filtro=icono.querySelector('filter');filtro.id='material-horizontal-'+i;const foto=icono.querySelector('image');foto.setAttribute('filter',`url(#${filtro.id})`);const clip=document.createElementNS('http://www.w3.org/2000/svg','clipPath');clip.id='recorte-material-'+i;const rect=document.createElementNS('http://www.w3.org/2000/svg','rect');rect.setAttribute('x','180');rect.setAttribute('y',tramos[i]);rect.setAttribute('width','365');rect.setAttribute('height',tramos[i+1]-tramos[i]);clip.append(rect);icono.querySelector('defs').append(clip);foto.setAttribute('clip-path',`url(#${clip.id})`);icono.setAttribute('aria-label',nombre);icono.removeAttribute('aria-hidden');return icono}));
  const materialesMovil=document.createElement('section');materialesMovil.className='materiales-resumen';materialesMovil.innerHTML='<div><p class="rotulo">Nuestros materiales</p><h2>De la estructura<br>al acabado.</h2><p>Todo para tu próximo proyecto.</p><a class="accion" href="#materiales">Ver catálogo de materiales ↗</a></div>';$('#cine').after(materialesMovil);
  const smallScreen=matchMedia('(max-width:640px)');function ubicaMateriales(){materialesMovil.hidden=!smallScreen.matches;$('.titular').append(materialesRail)}smallScreen.addEventListener('change',ubicaMateriales);ubicaMateriales();
  document.querySelectorAll('#servicios .servicio').forEach(card=>{const icon=iconosServicio[card.querySelector('h3').textContent];if(icon){const img=document.createElement('img');img.className='icono-servicio';img.src='img/servicio-'+icon+'.png';img.alt='';card.querySelector('.num').replaceWith(img)}});
  $('#cine').insertAdjacentHTML('afterend','<div class="confianza"><span><strong>+25 años</strong>En Aguascalientes</span><span><strong>A tu medida</strong>Corte y enchapado</span><span><strong>De la idea a la obra</strong>Asesoría personalizada</span><span><strong>Materiales y acabados</strong>Consulta nuestro catálogo</span></div>');
  const chips=document.createElement('div');chips.className='filtros';chips.setAttribute('aria-label','Filtrar líneas de producto');
  const labels=['Todos','Muebles','Muros y exterior','Construcción'];
  const cards=[...document.querySelectorAll('.linea')];const groups=[1,1,2,2,2,1,3,1,3];
  const count=document.createElement('p');count.className='resultado';count.setAttribute('aria-live','polite');
  $('.lineas').before(chips,count);
  labels.forEach((label,i)=>{const b=document.createElement('button');b.type='button';b.textContent=label;b.setAttribute('aria-pressed',String(i===0));chips.append(b);b.onclick=()=>{chips.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));cards.forEach((c,j)=>c.hidden=!!i&&groups[j]!==i);count.textContent=cards.filter(c=>!c.hidden).length+' líneas disponibles en el catálogo'};if(i===0)b.click()});
  const chosen=document.createElement('p');chosen.className='seleccion';chosen.hidden=true;chosen.setAttribute('aria-live','polite');$('#form-cotiza').prepend(chosen);
  function quote(material){
    const mapping={'WPC Lambrín':'WPC Lambrín (interior)','WPC Exterior':'WPC Exterior (deck o fachada)','Triplay y tableros':'Triplay o tablero','Enchapados y MDF natural':'Enchapado o MDF natural','Madera aserrada y polín':'Madera aserrada o polín'};
    const target=mapping[material]||material;
    const opt=[...$('#f-material').options].find(o=>o.textContent.toLowerCase()===target.toLowerCase());
    $('#f-material').value=opt?opt.value:'MDF Melamina';
    const detail=$('#f-detalle');detail.value='Me interesa: '+material+'.'+(detail.value?'\n'+detail.value:'');
    chosen.textContent='Seleccionaste: '+material;chosen.hidden=false;
    $('#cotiza').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});$('#f-nombre').focus({preventScroll:true});
  }
  cards.forEach(c=>{const b=document.createElement('button');b.type='button';b.className='accion';b.textContent='Cotizar esta línea ↗';b.onclick=()=>quote(c.querySelector('h3').textContent);c.querySelector('.linea-cuerpo').append(b)});
  const visor=document.createElement('dialog');visor.className='visor';visor.setAttribute('aria-labelledby','visor-titulo');visor.innerHTML='<button type="button" class="cerrar" aria-label="Cerrar imagen">Cerrar ×</button><img alt=""><h2 id="visor-titulo"></h2><p>Ambiente de referencia. Confirma el acabado y las medidas al cotizar.</p><button type="button" class="accion">Quiero este acabado ↗</button>';document.body.append(visor);
  visor.querySelector('.cerrar').onclick=()=>visor.close();visor.addEventListener('click',e=>{if(e.target===visor){const r=visor.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)visor.close()}});
  document.querySelectorAll('.toma').forEach(t=>{t.tabIndex=0;t.setAttribute('role','button');t.setAttribute('aria-label','Ampliar '+t.querySelector('img').alt);function open(){const img=t.querySelector('img'), title=t.querySelector('.acabado').textContent;visor.querySelector('img').src=img.src;visor.querySelector('img').alt=img.alt;$('#visor-titulo').textContent=title;visor.querySelector('.accion').onclick=()=>{visor.close();quote(title)};visor.showModal()}t.onclick=open;t.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();open()}}});
  $('#cotiza').insertAdjacentHTML('beforebegin','<section class="seccion faq" id="preguntas"><div class="envoltura"><div class="seccion-cabeza"><p class="rotulo">Antes de empezar</p><h2>Tu proyecto, con las cosas claras.</h2></div><details><summary>¿Qué necesito para pedir una cotización?</summary><p>Material o acabado, cantidad, medidas y ubicación de entrega. Si tienes un plano o lista de cortes, puedes adjuntarlo en WhatsApp.</p></details><details><summary>¿Pueden cortar y enchapar mi material?</summary><p>Sí. Consulta corte a medida y enchapado. Confirma con nuestro equipo el despiece, los cantos y el tiempo de preparación.</p></details><details><summary>¿Cómo elijo entre melamina, PET y WPC?</summary><p>Cuéntanos si tu proyecto es un mueble, un muro interior o un espacio exterior. Te ayudamos a elegir la línea adecuada para su uso.</p></details><details><summary>¿Los colores se ven igual que en pantalla?</summary><p>La iluminación y la pantalla pueden cambiar el color percibido. Revisa una muestra física y confirma el acabado antes de hacer tu pedido.</p></details></div></section>');
  const hora=[...document.querySelectorAll('.contacto-fila')].find(x=>x.textContent.includes('Horario'));if(hora)hora.querySelector('.valor').innerHTML='<a href="https://wa.me/524492050503?text=Hola%2C%20%C2%BFcu%C3%A1l%20es%20su%20horario%20de%20atenci%C3%B3n%3F" target="_blank" rel="noopener">Consulta el horario por WhatsApp ↗</a>';
  const address=[...document.querySelectorAll('.contacto-fila')].find(x=>x.textContent.includes('Dirección'));if(address)address.insertAdjacentHTML('beforeend','<a href="https://www.google.com/maps/search/?api=1&query=Harold%20R.%20Pape%20209%20Aguascalientes" target="_blank" rel="noopener">Cómo llegar ↗</a>');
  document.body.insertAdjacentHTML('beforeend','<div class="movil-cta"><span>¿Ya tienes una idea?</span><a class="accion" href="#cotiza">Cotizar proyecto ↗</a></div>');
  // El visor de Artifacts bloquea las descargas que inicia la propia pagina:
  // con [download] el enlace queda inerte. Se abre en pestana nueva y desde ahi se guarda.
  document.querySelectorAll('a[href="catalogo-bonaterra.pdf"]').forEach(a=>{a.removeAttribute('download');a.target='_blank';a.rel='noopener'});
  $('.btn-catalogo').lastChild.textContent=' Descargar catálogo · PDF 3.1 MB';
  $('#nota-form').setAttribute('role','status');
})();
