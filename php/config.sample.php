<?php
/**
 * Copia este archivo a config.php EN EL SERVIDOR y llena los valores.
 * config.php NO se sube al repositorio (está en .gitignore).
 *
 * Los datos de MySQL salen de cPanel → "Bases de datos MySQL":
 * el usuario y la base suelen llevar el prefijo de tu cuenta, p. ej.
 * "usuario_datara" y "usuario_leads".
 */

return [
    // --- MySQL (cPanel → Bases de datos MySQL) ---
    'db_host' => 'localhost',
    'db_name' => 'usuario_leads',
    'db_user' => 'usuario_datara',
    'db_pass' => 'PON_AQUI_LA_CONTRASEÑA',

    // --- Correo (buzón del dominio, cPanel → Cuentas de correo) ---
    // mail_from debe ser un buzón REAL de @datarahub.com para que Neubox
    // lo entregue con buen SPF/DKIM. mail_to es donde quieres recibir el aviso.
    'mail_from' => 'leads@datarahub.com',
    'mail_to'   => 'ing.antoniogz@gmail.com',

    // --- Rate limit ---
    'rate_limit_max'    => 5,      // envíos permitidos por ventana y por IP
    'rate_limit_window' => 3600,   // segundos (1 hora)

    // --- Privacidad ---
    // Cadena larga y aleatoria. Se usa para hashear la IP en el rate limit,
    // así nunca se guarda la IP en claro. Genera una con:  openssl rand -hex 32
    'ip_salt' => 'CAMBIA_ESTO_POR_UNA_CADENA_ALEATORIA_LARGA',
];
