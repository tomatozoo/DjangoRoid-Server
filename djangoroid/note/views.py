from django.shortcuts import render, get_object_or_404

from rest_framework import generics
from rest_framework import authentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView

from note.serializers import NoteListSerializer, NoteDetailSerializer, CanvasSerializer
from note.paginations import NoteListPagination
from note.permissions import IsNoteCreator, PublicOrIsNoteCreator
from note.models import Note, NoteToTag, Canvas, Page

from tag.models import Tag
from tag.serializers import TagSerializer

# from accounts.models import CustomUser
# from accounts.models import CustomUser as User
from django.contrib.auth import get_user_model  
User = get_user_model()

from comment.models import Comment


def get_user(request):
    try:
        token = request.META["HTTP_AUTHORIZATION"].split()[1]
    except:
        return Response(f"invalid token", status=status.HTTP_401_UNAUTHORIZED)
    user = Token.objects.get(key=token).user
    return user


def create_tag_note_objects(tags, note):
    for tag in tags:
        NoteToTag.objects.create(tag=Tag.objects.get(name=tag), note=note)


def get_page_number(image):
    # 0001_1.png
    file_name = image.split(".")[0]
    page_number_cand = file_name.split("_")
    return page_number_cand[len(page_number_cand)-1]


def process_two_image(background, handwriting):
    return handwriting


@api_view(['POST'])
def fork(request, *args, **kwargs):
    if request.method == 'POST':
        user = get_user(request)
        if not isinstance(user, User):
            return user
        user_id = kwargs['userPk']
        note_id = kwargs['notePk']
        note = get_object_or_404(
            Note, created_by=user_id, id=note_id, is_public=True)
        note.fork_count += 1
        note.save()
        new_note = Note.objects.create(title=note.title,
                                       description=note.description,
                                       created_by=user.id,
                                       is_public=note.is_public,
                                       history=user_id)
        new_note.save()
        return Response(data={'detail': 'fork'},
                        status=status.HTTP_201_CREATED)


class NoteListView(generics.ListAPIView):
    def get_queryset(self):
        user_id = self.kwargs['userPk']
        user = User.objects.get(id=user_id)
        notes = Note.objects.filter(created_by=user)
        return notes

    serializer_class = NoteListSerializer
    pagination_class = NoteListPagination


class NoteCreateView(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        user = get_user(request)
        if not isinstance(user, User):
            return user
        request.data['created_by'] = user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        note = serializer.save()
        if 'tags' in self.request.data:
            create_tag_note_objects(self.request.data['tags'], note)

    serializer_class = NoteDetailSerializer
    authentication_classes = [authentication.TokenAuthentication]

# 만약에 note가 private이면, 유저만 수정할 수 있음
#         만약 note가 public이면 로그인한 유저는 누구나 수정할 수 있음
#         만약에 delete method이면 생성한 유저만 삭제할 수 있음
#         contributor도 지정하기
class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    def get_object(self):
        user_id = self.kwargs['userPk']
        note_id = self.kwargs['notePk']
        note = get_object_or_404(Note, created_by=user_id, id=note_id)

        if self.request.method in permissions.SAFE_METHODS:
            return note
        
        if self.request.method == 'DELETE':
            self.check_object_permissions(self.request, note)
            return note
        
        if self.request.method in ['PATCH', 'PUT']:        
            if note.is_public:
                user = get_user(self.request)
                if not isinstance(user, User):
                    return "No permission"
                self.request.data['contributor'] = user.nickname
            else:
                self.check_object_permissions(self.request, note)

        return note

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance == "No permission":
            return Response(data={'detail' : "No permission(put, patch)"}, 
                            status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    serializer_class = NoteDetailSerializer
    permission_classes = [IsNoteCreator]
    # authentication_classes = [authentication.TokenAuthentication]


def get_user(request):
    try:
        token = request.META["HTTP_AUTHORIZATION"].split()[1]
    except:
        return Response(f"invalid token", status=status.HTTP_401_UNAUTHORIZED)
    user = Token.objects.get(key=token).user
    return user


class CanvasListCreateView(generics.ListCreateAPIView):
    serializer_class = CanvasSerializer
    queryset = Canvas.objects.all()

    def get_queryset(self):

        note_id = self.kwargs["notePk"]
        queryset = super().get_queryset().filter(
            note__id=note_id
        )
        return queryset

    def create(self, request, *args, **kwargs):
        ######################
        # validate request   #
        ######################
        # get user
        try:
            token = request.META["HTTP_AUTHORIZATION"].split()[1]
        except:
            return Response(f"invalid token", status=status.HTTP_401_UNAUTHORIZED)

        try:
            current_user = Token.objects.get(key=token).user
        except Token.DoesNotExist:
            return Response(data={"detail": "you do not have access to note"}, status=status.HTTP_401_UNAUTHORIZED)

        # 노트가 존재하며, public이거나 private이고 내 것인 경우
        note_id = kwargs.get("notePk")
        try:
            note_obj = Note.objects.get(id=note_id)
        except Note.DoesNotExist:
            return Response(data={"detail": "note does not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        # 노트가 존재하며, public이거나 private이고 내 것인 경우
        if not (note_obj.is_public or note_obj.created_by == current_user):
            return Response(data={"detail": "you do not have access to note"}, status=status.HTTP_401_UNAUTHORIZED)

        # 만약 canvas 객체가 이미 존재하면, 무시하기
        if note_obj.canvas is not None:
            return Response(data={"detail": "canvas object of the note already exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        # canvas 객체 만들기
        response = super().create(request, *args, **kwargs)

        print(response.data)

        canvas_id = response.data.get("id")
        canvas_obj = get_object_or_404(Canvas, id=canvas_id)

        # note와 연결하기
        note_obj.canvas = canvas_obj
        note_obj.save()

        # canvas에 image 연결하기
        images_urls = []
        images = request.data.pop("images", [])

        for image in images:
            page_number = get_page_number(image.name)
            new_image = Page.objects.create(page=page_number,
                                            canvas=canvas_obj,
                                            background=image,
                                            )
            images_urls.append([page_number, new_image.background.url])

        # return
        response.data["images"] = images_urls
        return response


class CanvasDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CanvasSerializer

    def patch(self, request, *args, **kwargs):
        ######################
        # validate request   #
        ######################
        # get user
        try:
            token = request.META["HTTP_AUTHORIZATION"].split()[1]
        except:
            return Response(f"invalid token", status=status.HTTP_401_UNAUTHORIZED)

        try:
            current_user = Token.objects.get(key=token).user
        except Token.DoesNotExist:
            return Response(data={"detail": "you do not have access to note"}, status=status.HTTP_401_UNAUTHORIZED)

        # 노트가 존재하며
        note_id = kwargs.get("notePk")
        try:
            note_obj = Note.objects.get(id=note_id)
        except Note.DoesNotExist:
            return Response(data={"detail": "note does not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        # 노트가 public이거나 private이고 내 것인 경우
        if not (note_obj.is_public or note_obj.created_by == current_user):
            return Response(data={"detail": "you do not have access to note"}, status=status.HTTP_401_UNAUTHORIZED)

        ################
        # canvas 업데이트하기
        ################
        canvas = note_obj.canvas

        # canvas에 image 연결하기
        images = request.data.pop("images", [])

        for image in images:
            page_number = get_page_number(image.name)
            # 이미 존재하는 페이지의 경우
            try:
                # 기본 이미지와 새 이미지를 더해 합성 이미지를 만들고 저장한다
                new_image = Page.objects.get(canvas=canvas, page=page_number)
                processed_image = process_two_image(
                    new_image,
                    image
                )
                new_image.background = processed_image
                new_image.save()

            # 존재하지 않는 페이지의 경우
            except Page.DoesNotExist:
                new_image = Page.objects.create(page=page_number,
                                                canvas=canvas,
                                                background=image,
                                                )

        # return
        serializer = CanvasSerializer(canvas)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
