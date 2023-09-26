"""initial migration

Revision ID: 794901bb414d
Revises: 
Create Date: 2023-09-05 20:30:43.919199

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '794901bb414d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pais',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('password_hash', sa.String(length=100), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('provincia',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('pais', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['pais'], ['pais.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('localidad',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('provincia', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['provincia'], ['provincia.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('persona',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('apellido', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('nacimiento', sa.Date(), nullable=False),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.Column('telefono', sa.Integer(), nullable=True),
    sa.Column('localidad', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['localidad'], ['localidad.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('persona')
    op.drop_table('localidad')
    op.drop_table('provincia')
    op.drop_table('user')
    op.drop_table('pais')
    # ### end Alembic commands ###
