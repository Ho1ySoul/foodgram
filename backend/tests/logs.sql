SELECT "authtoken_token"."key", "authtoken_token"."user_id", "authtoken_token"."created", "users_user"."id", "users_user"."password", "users_user"."last_login", "users_user"."is_superuser", "users_user"."is_staff", "user
s_user"."is_active", "users_user"."date_joined", "users_user"."first_name", "users_user"."last_name", "users_user"."email", "users_user"."username" FROM "authtoken_token" INNER JOIN "users_user" ON ("authtoken_token"."user_id" = "users_user"."id") WHERE "authtoken_token"."
key" = '229057368e67082ed220033d10596c2f577d5d57' LIMIT 21; args=('229057368e67082ed220033d10596c2f577d5d57',);


